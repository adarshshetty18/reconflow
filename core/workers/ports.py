from celery import Task
import os


class Ports(Task):
    name = 'core.ports'

    def run(self, *args, **kwargs):
        domain = args[0]
        update = args[1]
        os.popen(f"echo {domain} | naabu -nmap-cli 'nmap -sV -oX naabu-output' | tee /reconflow/ports/{domain}_ports.txt")\
            .read()
        update.reply_text(f"Here is the ports report for {domain}:")
        update.reply_document(open(f"/reconflow/ports/{domain}_ports.txt", 'rb'))
        return domain
