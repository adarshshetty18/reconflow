from celery import Task
import os


class Ports(Task):
    name = 'core.ports'

    def run(self, *args, **kwargs):
        domain = args[0]
        bot = args[1]
        chat_id = args[2]
        os.popen(f"echo {domain} | naabu -nmap-cli 'nmap -sV -oX naabu-output' | tee /reconflow/ports/{domain}_ports.txt")\
            .read()
        bot.send_message(chat_id=chat_id, text=f"Here is the ports report for {domain}:")
        bot.send_document(chat_id=chat_id, document=open(f"/reconflow/ports/{domain}_ports.txt", 'rb'))
        return domain
