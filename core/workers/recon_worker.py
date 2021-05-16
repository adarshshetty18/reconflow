import sys
from celery import Celery
from kombu import Queue
import logging

sys.path.append("/usr/src/reconflow/")
from workers.subdomains import Subdomains
from workers.livedomains import Livedomains
from workers.ports import Ports
from workers.directories import Directories

BROKER_URL = "redis://localhost:6379"

app = Celery(broker=BROKER_URL, backend=BROKER_URL)
app.conf['task_queues'] = (
        Queue("core"),
    )
app.conf['result_expires'] = 60*10

app.tasks.register(Subdomains())
app.tasks.register(Livedomains())
app.tasks.register(Ports())
app.tasks.register(Directories())

if __name__ == "__main__":
    logging.info('Initializing worker')
    app.start()
