from rq import Queue
from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime, timedelta

def func():
    print('running')

queue = Queue(connection=Redis())
scheduler = Scheduler(queue=queue, connection=queue.connection)
scheduler.run()

job = scheduler.enqueue_at(datetime.now(), func)
print('Job', job.id, job.origin, job.get_status())