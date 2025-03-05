from redis import Redis
from rq_scheduler import Scheduler

redis_conn = Redis()
scheduler = Scheduler(connection=redis_conn)

jobs = list(scheduler.get_jobs())
print(f"Found {len(jobs)} scheduled jobs")

for job in jobs:
    print(f"Job ID: {job.id}, Function: {job.func_name}, Origin: {job.origin}, Description: {job.description}")
