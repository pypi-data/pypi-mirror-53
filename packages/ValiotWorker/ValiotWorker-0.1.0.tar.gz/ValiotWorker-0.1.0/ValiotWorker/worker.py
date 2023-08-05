import pydash
import time
import json
from json.decoder import JSONDecodeError
import multiprocessing as mp
from datetime import datetime, timedelta
from enum import Enum
from pygqlc import GraphQLClient
from .Notifications import NotificationBehaviour
from .Logging import log, LogLevel
from . import uploaders
from . import queries
from . import mutations
from .dateHelpers import getUtcDate
from .croniterHelpers import get_croniter

gql = GraphQLClient()

class QueueType(Enum):
  EVENT= 'EVENT'
  FREQUENCY = 'FREQUENCY'
  ON_DEMAND = 'ON_DEMAND'
  SCHEDULE = 'SCHEDULE'

class JobStatus(Enum):
  ABORTED = 'ABORTED'
  ERROR = 'ERROR'
  FINISHED = 'FINISHED'
  PAUSED = 'PAUSED'
  RUNNING = 'RUNNING'
  WAITING = 'WAITING'

queues = {}

def job(
  name, 
  alias, 
  description='', 
  schedule='', 
  enabled=None, 
  queueType=QueueType.ON_DEMAND, 
  notificationBehaviour=NotificationBehaviour.DEFAULT,
  notificationFrequency = '',
  notificationSchedule = ''
  ):
  def wrap(f):
    parameters = {
      'name': name,
      'alias': alias,
      'description': description,
      'schedule': schedule,
      'type': queueType.value,
      'function': f,
      "last_run_at": datetime.now()
    }
    if enabled is not None:
      parameters['enabled'] = enabled
    queues[name] = parameters
    return f
  return wrap

def not_found(job_id, update_job, kwargs):
  from botella.helpers.ValiotWorker.Notifications import nextNotifOld
  log(LogLevel.ERROR, 'Function not found :(')
  message= 'Funcion no habilitada, favor de contactar a administrador'
  notificationData = {}
  if(nextNotifOld(kwargs['job'])): 
    data, errors = gql.mutate(mutations.create_notification, {
      'context': 'DANGER',
      'title': f'Error en {kwargs["job"]["queue"]["alias"]}',
      'content': message,
      'metadata': json.dumps({"resolved": False}),
    })
    now = getUtcDate(datetime.now())
    nextNotifDate = now + timedelta(minutes=20)
    notificationData = {
      'id': data['result']['id'],
      'Sent': True,
      'SentAt': now.strftime("%Y-%m-%dT%H:%M:%SZ"),
      # 'frequency': '*/2 * * * *', # cron descriptor or empty string
      'sendNextAt': nextNotifDate.strftime("%Y-%m-%dT%H:%M:%SZ"), # cron descriptor or empty string
    }
  update_job({
    'id': job_id,
    'status': 'ERROR',
    'output': json.dumps({
      'notification': notificationData,
      'message': message
    })
  })

# Run helpers: -------------------------------
def getJobData(job):
  NOT_FOUND = {
    'alias': 'Funcion no encontrada',
    'description': 'Funcion ejecutada cuando se trata de llamar Job sin una función registrada',
    'schedule': None,
    'enabled': True,
    'type': QueueType.ON_DEMAND,
    'function': not_found,
    "last_run_at": datetime.now()
  }
  fn_name = pydash.get(job, 'queue.name', 'NOT_FOUND')
  job_dict = pydash.get(queues, fn_name, NOT_FOUND)
  return fn_name, job_dict

def runJob(job, context):
  # Obtiene job
  fn_name, job_dict = getJobData(job)
  log(LogLevel.INFO, f"running {fn_name}")
  job_fn = job_dict['function']
  # Obtiene inputs
  if job['input']:
    try:
      kwargs = json.loads(job['input'])
    except JSONDecodeError as e:
      # falló al leer datos de input, aborta mision
      variables = {
        'id': int(job['id']),
        'status': 'ERROR',
        'output': f'Job input error: {str(e)}'
      }
      uploaders.update_job(variables)
      log(LogLevel.ERROR, e)
      return
  else:
    kwargs = job_dict
  # try to run job
  kwargs['enabled'] = job['queue']['enabled']
  kwargs['name'] = fn_name
  kwargs['schedule'] = job['queue']['schedule']
  # ! Inyecta a los kwargs el job que se está ejecutando:
  kwargs['job'] = job
  variables = {
    'id': int(job['id']),
    'queueName': job['queue']['name'],
    'status': 'RUNNING',
    'lastRunAt': getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
  }
  data, errors = gql.mutate(mutation=mutations.run_job, variables=variables)
  if (
      pydash.get(data, 'updateJob.successful') 
      and pydash.get(data, 'updateQueue.successful')
    ):
    p = context.Process(
      target=job_fn, 
      args=(int(job['id']), uploaders.update_job, kwargs)
    )
    p.start()
    log(LogLevel.SUCCESS, f'started job with ID {job["id"]}')

def processJobs(context):
  jobs, errors = gql.query(queries.all_jobs)
  if errors:
    message = errors[0]
    log(LogLevel.ERROR, f'Error! msg: {message}')
    return
  if jobs is not None and len(jobs) > 0:
    log(LogLevel.WARNING, f"Found {len(jobs)} jobs")
    for job in jobs:
      if job['queue']['enabled']:
        runJob(job, context)
  else:
    log(LogLevel.WARNING, "Listening...")

def deleteStaleJobs():
  jobs, errors = gql.query(queries.waiting_jobs)
  if (len(jobs) > 0):
    log(LogLevel.ERROR, f'Deleting {len(jobs)} stale jobs:')
    for job in jobs:
      result, errors = gql.mutate(mutations.delete_job, {'id': job['id']})
      if (not errors):
        log(LogLevel.ERROR, f'deleted stale job {job["id"]}:')
      else:
        log(LogLevel.ERROR, f'errors deleting stale job: {errors}')

def updateAvailableQueues():
  log(LogLevel.SUCCESS, 'Actualizando Jobs disponibles')
  for name, queue in queues.items():
    enabled= pydash.get(queue, 'enabled', None)
    description = pydash.get(queue, 'description', None)
    schedule= pydash.get(queue, 'schedule', None)
    query= pydash.get(queue, 'query', None)
    variables = {
      'name':queue['name'],
      'alias':queue['alias'],
      'type': queue['type'],
    }
    # ! Add optional variables
    if enabled is not None:
      variables['enabled'] = enabled
    if description:
      variables['description'] = description
    if schedule:
      variables['schedule'] = schedule
    if query:
      variables['query'] = query
    data, errors = gql.mutate(
      mutation=mutations.upsert_queue,
      variables=variables
    )
    if (errors):
      log(LogLevel.ERROR, f'Error actualizando Queue {name}.')
      log(LogLevel.ERROR, errors)
    else:
      log(LogLevel.SUCCESS, f'Queue {name} actualizado correctamente')

def runFrequencyQueues(queues):
  from pytz import timezone
  utc = timezone("UTC")
  queuesByType = pydash.group_by(queues, 'type')
  freqQueues = queuesByType['FREQUENCY']
  # log(LogLevel.WARNING, f'checking {len(freqQueues)} frequency queues')
  for queue in freqQueues:
    # if it has never been ran, set the lastRunAt as a very old date (forces next run)
    lastRunAt = pydash.get(queue, 'lastRunAt', None)
    if not lastRunAt:
      lastRunDate = datetime(2000, 1, 1)
    else:
      lastRunDate = datetime.strptime(lastRunAt, "%Y-%m-%dT%H:%M:%SZ")
    lastRunDate = utc.localize(lastRunDate)
    now = getUtcDate(datetime.now())
    cron_iter = get_croniter(queue['schedule'], now)
    nextRunAt = [cron_iter.get_next(datetime) for _ in [0, 1]] # next and nexter dates
    #validate if next date is met:
    elapsedFromLastRun = (now - lastRunDate).total_seconds() / 60.0 # in minutes
    freq = (nextRunAt[1] - nextRunAt[0]).total_seconds() / 60.0 # in minutes
    if (elapsedFromLastRun > freq):
      # ! Run the frequency job!
      if (queue["enabled"]):
        gql.mutate(
          mutation=mutations.create_job,
          variables={ 'queueName': queue['name'] }
        )

def eventLoop(context, interval=1.0):
  try:
    queues, errors = gql.query(queries.all_queues)
    runFrequencyQueues(queues)
    # TODO: sendReminders(queues)
    processJobs(context=context)
  except Exception as e:
    log(LogLevel.ERROR, f"Error in worker's event loop!")
    log(LogLevel.ERROR, f'e: {e}')
  time.sleep(interval)

def run():
  context = mp.get_context('fork')
  deleteStaleJobs()
  updateAvailableQueues()
  while 1:
    eventLoop(context)
