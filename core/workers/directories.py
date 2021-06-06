from celery import Task
import os


class Directories(Task):
    name = 'core.directories'

    def run(self, *args, **kwargs):
        domain = args[0]
        os.popen(f'ffuf -w "/reconflow/livedomains/{domain}.txt:DOMAIN" -w /usr/src/reconflow/wordlists/dicc.txt '
                 f'-u DOMAIN/FUZZ -t 4000 -mc 200 -of json -o /reconflow/directories/{domain}_dirs.json').read()
        return domain
