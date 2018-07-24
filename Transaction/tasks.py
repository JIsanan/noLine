from noLine.celery import app
from Company.models import Company
from Service.models import Service
from Teller.models import Teller
from Transaction.models import Transaction
from ComputedServiceTime.models import ComputedServiceTime
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import numpy

from noLine.settings import API_KEY, API_SECRET
import nexmo

client = nexmo.Client(key=API_KEY, secret=API_SECRET)


@app.task
def learn():
    Companylist = Company.objects.all()
    for company in Companylist:
        services = Service.objects.filter(company=company)
        for service in services:
            learnservice(service)


@app.task
def lining():
    Companylist = Company.objects.all()
    for company in Companylist:
        services = Service.objects.filter(company=company)
        for service in services:
            queue(service)


def learnservice(service):
    last_month = datetime.today() - timedelta(days=30)
    logs = Transaction.objects.filter(time_ended__gte=last_month).all()
    lists = []
    for i in logs:
        lists.append(i.log)
    std = numpy.std(lists, axis=0)
    ave = numpy.mean(lists, axis=0)
    var = numpy.var(lists, axis=0)
    drift = ave - (var / 2)
    service = ComputedServiceTime.objects.filter(Service=service).first()
    service.std = std
    service.var = drift
    service.save()


def queue(service):
    userInQueue = Transaction.objects.filter(status='A', time_started=None, service=service).order_by('time_joined').all()
    tellers = Teller.objects.filter(service=service)
    telleravail = tellers.filter(is_active=True, availability=True, service=service).all()
    telleravailactiveornot = tellers.filter(is_active=True, service=service).all()
    tellernotavail = tellers.filter(is_active=False, service=service).all()
    if telleravail.count() > 0:
        time = []
        for i in range(0,tellers.count()):
            time.append(0)
        for i in tellernotavail:
            time[i.teller_number] = 99999999
        idx = 0
        user = 0
        layer = get_channel_layer()
        for idx, i in enumerate(telleravail):
            if userInQueue.count() > idx:
                time[i.teller_number] += userInQueue[idx].computed_time
                i.transaction = userInQueue[idx]
                i.availability = False
                user = userInQueue[idx]
                user.time_started = datetime.now()
                user.save()
                i.save()
                async_to_sync(layer.group_send)('teller_' + str(service.pk), {
                    'type': 'get.newcustomer',
                    'tellerpk': i.pk,
                    'pk': user.pk,
                    'priority_num': user.priority_num,
                })
                async_to_sync(layer.group_send)('transaction_' + str(service.pk), {
                    'type': 'get.usersturn',
                    'transpk': user.pk,
                    'teller_no': i.teller_number,
                })
        userInQueue = userInQueue[idx:]
        async_to_sync(layer.group_send)('teller_' + str(service.pk), {
            'type': 'get.changeofamount',
            'amount': userInQueue.count() 
        })
        async_to_sync(layer.group_send)('kiosk_' + str(service.pk), {
            'type': 'get.changeofline',
            'servicepk': service.company.pk,
            'amount': userInQueue.count() 
        })
        print("HELLO HELLO")
        for c,i in enumerate(userInQueue):
            print(time)
            indx = numpy.argmin(time)
            predicted = i.computed_time
            t = datetime.now() + timedelta(seconds=time[indx])
            print(t.strftime("%Y-%m-%d %H:%M:%S"))
            if i.when_to_notify and (i.when_to_notify >= c + 1):
                i.when_to_notify = 0
                i.save()
                client.send_message({'from': 'noLine', 'to': i.phone_num, 'text': 'It is almost your turn.'+'\nETA:\n'+t.strftime("%Y-%m-%d %H:%M:%S")+'\n'})
            async_to_sync(layer.group_send)('transaction_' + str(service.pk), {
                'type': 'get.changeofeta',
                'transpk': i.pk,
                'eta': t.strftime("%Y-%m-%d %H:%M:%S"),
                'priority_num': user.priority_num,
                'count': userInQueue.count(),
            })
            time[indx] += predicted
        userInReserved = Transaction.objects.filter(status='R', service=service).all()
        for i in userInReserved:
            indx = numpy.argmin(time)
            if time[indx] == 99999999:
                time[indx] = 0
            t = datetime.now() + timedelta(seconds=time[indx])
            async_to_sync(layer.group_send)('transaction_' + str(service.pk), {
                'type': 'get.changeofeta',
                'transpk': i.pk,
                'eta': t.strftime("%Y-%m-%d %H:%M:%S"),
                'priority_num': user.priority_num,
                'count': userInQueue.count(),
            })
    elif(telleravailactiveornot.count() > 0):
        userInQueue = Transaction.objects.filter(status='A', time_started=None, service=service).order_by('time_joined').all().count()
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('teller_' + str(service.pk), {
            'type': 'get.changeofamount',
            'amount': userInQueue
        })
        async_to_sync(layer.group_send)('kiosk_' + str(service.pk), {
            'type': 'get.changeofline',
            'servicepk': service.company.pk,
            'amount': userInQueue 
        })
