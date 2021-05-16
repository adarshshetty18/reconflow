from celery import Task
import os


class Livedomains(Task):
    name = 'core.subdomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        os.popen(f"cat /reconflow/subdomains/{domain}.txt | httpx -silent | tee /reconflow/livedomains/{domain}.txt")\
            .read()
        return domain
