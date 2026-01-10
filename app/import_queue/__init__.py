import os
from bullmq import Queue

JOB_QUEUE_NAME = os.environ['JOB_QUEUE_NAME']
JOB_QUEUE_CONNECTION = os.environ['JOB_QUEUE_CONNECTION']

queue = Queue(JOB_QUEUE_NAME, { "connection": JOB_QUEUE_CONNECTION })

async def trigger_report_import(uid: str):
    await queue.add('report-import', { "uid": uid })
