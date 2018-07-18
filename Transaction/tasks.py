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


@app.task
def learn():
    service = Service.objects.filter(pk=1).first()
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


@app.task
def lining():
    Companylist = Company.objects.all()
    for company in Companylist:
        services = Service.objects.filter(company=company)
        for service in services:
            queue(service)


def queue(service):
    userInQueue = Transaction.objects.filter(status='A', time_started=None, service=service).order_by('time_joined').all()
    tellers = Teller.objects.filter(service=service)
    telleravail = tellers.filter(is_active=True, availability=True, service=service).all()
    if telleravail.count() > 0:
        time = []
        for i in range(0,tellers.count()):
            time.append(0)
        idx = 0
        for idx, i in enumerate(telleravail):
            if userInQueue.count() > idx:
                time[i.teller_number] += userInQueue[idx].computed_time
                i.transaction = userInQueue[idx]
                i.availability = False
                user = userInQueue[idx]
                user.time_started = datetime.now()
                user.save()
                i.save()
                layer = get_channel_layer()
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
        print(idx)
        userInQueue = userInQueue[idx:]
        print(userInQueue.count())
        for i in userInQueue:
            print("yawaaa")
            indx = numpy.argmin(time)
            predicted = i.computed_time
            time[indx] += predicted
            t = datetime.now() + timedelta(seconds=time[indx])
            async_to_sync(layer.group_send)('transaction_' + str(service.pk), {
                'type': 'get.changeofeta',
                'transpk': i.pk,
                'eta': t.strftime("%Y-%m-%d %H:%M:%S"),
                'priority_num': user.priority_num,
                'count': userInQueue.count(),
            })
