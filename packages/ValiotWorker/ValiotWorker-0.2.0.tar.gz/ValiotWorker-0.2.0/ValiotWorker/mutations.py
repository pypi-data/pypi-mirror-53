create_job = '''
  mutation createJob(
    $queueName: String!
    $worker: String
  ){
    createJob(
      queueName: $queueName
      workerCode: $worker
      jobStatus: WAITING
      progress: 0
      input: "{}"
      output: "{}"
    ){
      successful
      messages{
        message
        field
      }
      result{
        id
        input
        output
        jobStatus
        progress
        queue{
          id
          name
          updatedAt
        }
      }
    }
  }
'''

update_job='''
  mutation UpdateJob(
    $id: ID!
    $status: JobStatus!
    $output: Text!
    $progress: Int
  ) {
    updateJob(
      id: $id
      job: {
        jobStatus: $status
        progress: $progress
        output: $output
      }
    ) {
      successful
      result {
        id
      }
      messages {
        message
      }
    }
  }
'''

delete_job='''
  mutation deleteJob($id: ID!) {
    deleteJob(id: $id) {
      successful
      messages{
        field
        message
      }
      result{
        id
      }
    }
  }
'''

upsert_queue='''
mutation upsertQueue(
  $name: String!
  $alias: String!
  $type: QueueType!
  $enabled: Boolean
  $description: Text
  $schedule: String
  $query: Text
) {
  upsertQueue(
    name: $name
    queue: {
      alias: $alias
      type: $type
      enabled: $enabled
      description: $description
      schedule: $schedule
      query: $query
    }
  ) {
    successful
    result {
      id
      name
      alias
      description
      schedule
      enabled
      type
    }
    messages {
      message
      field
    }
  }
}
'''

run_job = '''
  mutation runJob(
    $id: ID!
    $status: JobStatus!
    $queueName: String!, 
    $lastRunAt: DateTime!
  ) {
    updateJob(
      id: $id
      job: {
        jobStatus: $status
        progress: 0
        output: "{}"
        }
    ) {
      successful
      messages { field message }
      result { id jobStatus progress }
    }
    updateQueue(
      findBy: { name: $queueName },
      queue: { lastRunAt: $lastRunAt }
    ) {
      successful
      messages { field message }
      result { id name lastRunAt }
    }
  }
'''

create_notification = '''
mutation CreateNotification(
  $context: NotificationType,
  $title: String,
  $content: Text,
  $link: String,
  $metadata: String,
  $linkText: String
){
  createNotification(
    read: false
    context: $context
    title: $title
    content: $content
    link: $link
    linkText: $linkText
    metadata: $metadata
  ){
    successful
    result{
      id
      title
      content
      context
      metadata
      insertedAt
      updatedAt
    }
    messages{
      message
    }
  }
}
'''

'''
Queue metadata:
{
  "reminder": {
    "id": "123"
    "SentAt": "2019-07-26T12:51:16Z",
    # ! The reminder is sent without a RESOLVED prop
    "enabled": true,
  },
  "notification": {
    "id": "121"
    "title": "blabla",
    "content": "this is notification",
    "context": "DANGER",
    "metadata": "..." # ! If this function is used to create notifications, we assume a "resolved: false" must be sent with it
  }
}
'''
update_queue_meta = '''
  mutation updateQueueMetadata(
    $queueName: String!
    $metadata: Text!
  ){
    updateQueue(
      findBy:{name: $queueName}
      queue:{
        query: $metadata
      }
    ){
      successful
      messages{
        message
        field
      }
      result{
        id
        name
        alias
        description
        enabled
        schedule
        query
      }
    }
  }
'''

update_notification_metadata = '''
  mutation updateMetadata(
    $id: ID!
    $metadata: String!
  ){
    updateNotification(
      id:$id
      notification:{
        metadata: $metadata
      }
    ){
      successful
      messages{
        field
        message
      }
      result{
        id
        read
        title
        content
        context
        metadata
        insertedAt
        updatedAt
      }
    }
  }
'''
