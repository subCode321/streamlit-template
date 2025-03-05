from rq import Queue
from redis import Redis

def add_process_to_queue(task):
    queue = Queue(connection=Redis())
    job = queue.enqueue(task)
    print('Job added to queue', job.id, job.get_status())