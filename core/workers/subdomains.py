from celery import Task


class Subdomains(Task):
    name = 'core.subdomains'

    def run(self, *args, **kwargs):
        pass
