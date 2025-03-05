# run_scheduler.py
from redis import Redis
from rq_scheduler import Scheduler

def start_scheduler():
    redis_conn = Redis()
    scheduler = Scheduler(connection=redis_conn)

    print("Starting RQ Scheduler...")
    scheduler.run()

if __name__ == "__main__":
    start_scheduler()
