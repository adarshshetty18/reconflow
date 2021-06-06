from celery import Task
import os


class Subdomains(Task):
    name = 'core.subdomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        os.popen(f"subfinder -d {domain} -o /reconflow/subdomains/{domain}_sdomains.txt").read()
        return domain
