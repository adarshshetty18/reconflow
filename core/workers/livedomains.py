from celery import Task
import os
from telegram.ext import Updater
TOKEN = os.environ["TOKEN"]


class Livedomains(Task):
    name = 'core.livedomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        chat_id = args[1]
        updater = Updater(TOKEN, use_context=True)
        os.popen(f"cat /reconflow/subdomains/{domain}_sdomains.txt | httpx -silent | tee /reconflow/livedomains/{domain}_ldomains.txt")\
            .read()
        updater.bot.send_document(chat_id=chat_id, caption=f"Here is the livedomains report for {domain}:",
                                  document=open(f"/reconflow/livedomains/{domain}_ldomains.txt", 'rb'))
        return domain
