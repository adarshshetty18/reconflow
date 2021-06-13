from celery import Task
import os


class Livedomains(Task):
    name = 'core.livedomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        update = args[1]
        os.popen(f"cat /reconflow/subdomains/{domain}_sdomains.txt | httpx -silent | tee /reconflow/livedomains/{domain}_ldomains.txt")\
            .read()
        update.reply_text(f"Here is the livedomains report for {domain}:")
        update.reply_document(open(f"/reconflow/livedomains/{domain}_ldomains.txt", 'rb'))
        return domain
