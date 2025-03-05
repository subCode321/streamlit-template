from redis import Redis
from rq import Queue

queue = Queue(connection=Redis())

jobs = queue.jobs
print(f"Found {len(jobs)} jobs in the default queue")

for job in jobs:
    print(f"Job ID: {job.id}, Function: {job.func_name}, Description: {job.description}")
