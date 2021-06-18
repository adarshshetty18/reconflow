from celery import Task
import os
from telegram.ext import Updater
TOKEN = os.environ["TOKEN"]


class Ports(Task):
    name = 'core.ports'

    def run(self, *args, **kwargs):
        domain = args[0]
        chat_id = args[1]
        updater = Updater(TOKEN, use_context=True)
        os.popen(f"echo {domain} | naabu -nmap-cli 'nmap -sV -oX naabu-output' | tee /reconflow/ports/{domain}_ports.txt")\
            .read()
        updater.bot.send_document(chat_id=chat_id, caption=f"Here is the ports report for {domain}:",
                                  document=open(f"/reconflow/ports/{domain}_ports.txt", 'rb'))
        return domain
