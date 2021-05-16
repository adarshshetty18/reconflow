from celery import Task
import os


class Ports(Task):
    name = 'core.ports'

    def run(self, *args, **kwargs):
        domain = args[0]
        os.popen(f"echo {domain} | naabu -nmap-cli 'nmap -sV -oX naabu-output' | tee /reconflow/ports/{domain}.txt")\
            .read()
        return domain