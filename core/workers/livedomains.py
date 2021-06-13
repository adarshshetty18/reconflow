from celery import Task
import os


class Livedomains(Task):
    name = 'core.livedomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        bot = args[1]
        chat_id = args[2]
        os.popen(f"cat /reconflow/subdomains/{domain}_sdomains.txt | httpx -silent | tee /reconflow/livedomains/{domain}_ldomains.txt")\
            .read()
        bot.send_message(chat_id=chat_id, text=f"Here is the livedomains report for {domain}:")
        bot.send_document(chat_id=chat_id, document=open(f"/reconflow/livedomains/{domain}_ldomains.txt", 'rb'))
        return domain
