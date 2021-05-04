import sys
from celery import Celery
from kombu import Queue
import logging

sys.path.append("/usr/src/reconflow/core")
from jobs.subdomains import Subdomains

BROKER_URL = "redis://localhost:6379"

app = Celery(broker=BROKER_URL, backend=BROKER_URL)
app.conf['core'] = (
    Queue('job_queue')
)
app.conf['result_expires'] = 60*10

app.tasks.register(Subdomains())

if __name__ == "__main__":
    logging.info('Initializing worker')
    app.start()
