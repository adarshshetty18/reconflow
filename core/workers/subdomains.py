from celery import Task
import os
from telegram.ext import Updater
TOKEN = os.environ["TOKEN"]


class Subdomains(Task):
    name = 'core.subdomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        chat_id = args[1]
        updater = Updater(TOKEN, use_context=True)
        os.popen(f"subfinder -d {domain} -o /reconflow/subdomains/{domain}_sdomains.txt").read()
        updater.bot.send_message(chat_id=chat_id, text=f"Here is the subdomains report for {domain}:")
        updater.bot.send_document(chat_id=chat_id, document=open(f"/reconflow/subdomains/{domain}_sdomains.txt", 'rb'))
        return domain
