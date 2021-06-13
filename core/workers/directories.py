from celery import Task
import os


class Directories(Task):
    name = 'core.directories'

    def run(self, *args, **kwargs):
        domain = args[0]
        update = args[1]
        os.popen(f'ffuf -w "/reconflow/livedomains/{domain}_ldomains.txt:DOMAIN" -w /usr/src/reconflow/wordlists/dicc.txt '
                 f'-u DOMAIN/FUZZ -t 4000 -mc 200 -of json -o /reconflow/directories/{domain}_dirs.json').read()
        update.message.reply_text(f"Here is the directories report for {domain}:")
        update.message.reply_document(open(f"/reconflow/directories/{domain}_dirs.json", 'rb'))
        return domain
