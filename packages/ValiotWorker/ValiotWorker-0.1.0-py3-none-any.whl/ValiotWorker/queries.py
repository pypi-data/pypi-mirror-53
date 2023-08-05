all_jobs='''
{
    jobs(
        orderBy: { asc: ID }, 
        filter: { jobStatus: WAITING }
    ) {
        id
        input
        output
        progress
        jobStatus
        queue {
          id
          name
          alias
          type
          enabled
          schedule
          query
        }
    }
}
'''

waiting_jobs = '''
query {
  jobs(filter: { jobStatus: WAITING }) {
    id
    input
    output
    progress
    queue {
      id
      name
      alias
      type
      enabled
      schedule
      query
    }
  }
}
'''

get_job ='''
query GetJob(
  $id: ID!
){
    job(
        id: $id
    ) {
        id
        input
        output
        jobStatus
        queue {
          id
          name
          alias
          type
          enabled
          schedule
          query
        }
    }
}
'''

get_queue = '''
query QueueByName(
  $queueName: String
)
{
  queue(
    findBy:
    {name: $queueName}
  ){
    id
    name
    alias
    type
    enabled
    schedule
    query
  }
}
'''

all_queues = '''
{
  queues{
    id
    name
    alias
    description
    enabled
    type
    schedule
    query
    lastRunAt
    updatedAt
    insertedAt
  }
}
'''

get_queue_last_jobs = '''
query QueueLastJobs(
  $name: String!
  $count: Int!
){
  queue(
    findBy: {
      name:$name
    }
  ){
    id
    name
    alias
    enabled
    jobs(
      orderBy:
      {desc: INSERTED_AT}
      limit: $count
    ){
      id
      jobStatus
      output
    }
  }
}
'''

get_queue_last_job = '''
query QueueLastJob(
  $name: String!
){
  queue(
    findBy: {
      name:$name
    }
  ){
    id
    name
    alias
    enabled
    jobs(
      orderBy:
      {desc: INSERTED_AT}
      limit: 1
    ){
      id
      jobStatus
      output
    }
  }
}
'''

get_notification = '''
  query getNotification($id: ID!){
    notification(id: $id){
      id
      title
      content
      context
      read
      metadata
      insertedAt
    }
  }
'''