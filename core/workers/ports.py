from celery import Task
import os


class Ports(Task):
    name = 'core.ports'

    def run(self, *args, **kwargs):
        domain = args[0]
        os.popen(f"cat /reconflow/livedomains/{domain}.txt |naabu -silent | tee /reconflow/ports/{domain}.txt")\
            .read()
        return domain