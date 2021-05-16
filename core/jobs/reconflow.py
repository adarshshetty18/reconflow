from celery import Celery
from celery import chain
capp = Celery(broker="redis://localhost:6379", backend="redis://localhost:6379")
capp.conf['result_expires'] = 60*10

domain = "hackerone.com"

sig_list = []
sub_sig = capp.signature('core.subdomains', debug=True, args=[domain]).set(queue='core')
sig_list.append(sub_sig)

live_sig = capp.signature('core.livedomains', debug=True, args=[]).set(queue='core')
sig_list.append(live_sig)

ports_sig = capp.signature('core.ports', debug=True, args=[]).set(queue='core')
sig_list.append(ports_sig)

dir_sig = capp.signature('core.directories', debug=True, args=[]).set(queue='core')
sig_list.append(dir_sig)

chain(sig_list).apply_async()
print("Job invoked")
