from celery import Task
import os


class Livedomains(Task):
    name = 'core.livedomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        os.popen(f"cat /reconflow/subdomains/{domain}_sdomains.txt | httpx -silent | tee /reconflow/livedomains/{domain}_ldomains.txt")\
            .read()
        return domain
