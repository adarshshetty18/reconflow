from celery import Task
import os


class Subdomains(Task):
    name = 'core.subdomains'

    def run(self, *args, **kwargs):
        domain = args[0]
        update = args[2]
        os.popen(f"subfinder -d {domain} -o /reconflow/subdomains/{domain}_sdomains.txt").read()
        update.message.reply_text(f"Here is the subdomains report for {domain}:")
        update.message.reply_document(open(f"/reconflow/subdomains/{domain}_sdomains.txt", 'rb'))
        return domain
