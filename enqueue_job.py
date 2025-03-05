# enqueue_job.py
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime, timedelta
from tasks import sample_job, sample_job_2

def enqueue_immediate():
    redis_conn = Redis()
    queue = Queue(connection=redis_conn)
    queue.enqueue_at(datetime.now() + timedelta(seconds=5), sample_job)
    print("✅ Immediate job enqueued!")

def schedule_future():
    redis_conn = Redis()
    scheduler = Scheduler(connection=redis_conn)

    run_time = datetime.now() + timedelta(seconds=5)  # Schedule 30 seconds later
    scheduler.enqueue_at(run_time, sample_job_2)
    print(f"✅ Job scheduled to run at {run_time}")

enqueue_immediate()


