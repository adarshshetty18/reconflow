from celery import Task
import os
from telegram.ext import Updater
TOKEN = os.environ["TOKEN"]


class Directories(Task):
    name = 'core.directories'

    def run(self, *args, **kwargs):
        domain = args[0]
        chat_id = args[1]
        updater = Updater(TOKEN, use_context=True)
        os.popen(f'ffuf -w "/reconflow/livedomains/{domain}_ldomains.txt:DOMAIN" -w /usr/src/reconflow/wordlists/dicc.txt '
                 f'-u DOMAIN/FUZZ -t 4000 -mc 200 -of json -o /reconflow/directories/{domain}_dirs.json').read()
        updater.bot.send_message(chat_id=chat_id, text=f"Here is the directories report for {domain}:")
        updater.bot.send_document(chat_id=chat_id, document=open(f"/reconflow/directories/{domain}_dirs.json", 'rb'))
        return domain
