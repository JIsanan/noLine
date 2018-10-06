from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from Service.models import Service
from Service.serializer import ServiceSerializer
from Service.serializer import ServiceETASerializer
from Teller.models import Teller
from Company.models import Company
from Transaction.models import Transaction
from ComputedServiceTime.models import ComputedServiceTime
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from datetime import datetime, date, timedelta
from scipy.stats import norm
from math import e
import random
import numpy
import uuid
import re

from noLine.settings import API_KEY, API_SECRET
import nexmo

client = nexmo.Client(key=API_KEY, secret=API_SECRET)


class TransactionViewSet(ViewSet, APIView):

    def list(self, request):
        return Response("none")

    @action(methods=['post'], detail=False)
    def authenticate(self, request):
        retList = {}
        retList['teller_no'] = ''
        mac = Transaction.objects.filter(Q(mac=request.data['mac']), Q(status='A') | Q(status='R')).first()
        if mac and request.data['uuid'] == '':
            uuidvar = mac.mac
            check = mac
            uuidvar = mac.uuid
        else:
            uuidvar = request.data['uuid']
            UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
            if not UUID_PATTERN.match(uuidvar):
                retList['message'] = 'not a valid customer'
                return Response(retList)
            check = Transaction.objects.filter(uuid=uuid.UUID(uuidvar).hex).first()
        if check.mac is not None and check.mac != request.data['mac']:
            retList['message'] = 'not your device'
            return Response(retList)
        if not check or check.status == 'C':
            retList['message'] = 'not a valid customer'
            return Response(retList)
        if not mac or (mac.uuid == check.uuid):
            if check.mac is None:
                check.mac = request.data['mac']
                check.save()
        else:
            retList['message'] = 'not unique'
            return Response(retList)
        service = Service.objects.filter(pk=check.service.pk).first()
        retList['service_id'] = service.pk
        retList['service_name'] = service.service_name
        retList['company_name'] = service.company.company_name
        currentserved = Transaction.objects.filter(status='A', service=service, time_ended=None).exclude(time_started=None).order_by('-time_started').first()
        if not currentserved:
            currentserved = 'none'
        else:
            currentserved = currentserved.priority_num
        retList['current_served'] = currentserved
        if check.time_started is not None and check.status == 'A':
            retList['message'] = 'it is your turn'
            retList['teller_no'] = check.teller.first().teller_number
            retList['time_joined'] = check.time_joined.strftime("%Y-%m-%dT%H:%M:%S")
            retList['waiting_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            retList['priority_number'] = check.priority_num
            retList['uuid'] = uuidvar
            return Response(retList)
        elif check.status == 'S':
            retList['message'] = 'you have been skipped'
            return Response(retList)
        elif check.status == 'CP':
            retList['message'] = 'your transaction is already complete'
            return Response(retList)
        elif check.status == 'R':
            retList['message'] = 'you are in reserved'
        else:
            retList['message'] = "successfully logged in"   
        user_in_line = Transaction.objects.filter(status='A', service=service).order_by('time_joined').all()
        tellers = service.teller.count()
        tellersnotavail = service.teller.filter(is_active=False).all()
        time = []
        if tellersnotavail.count() == tellers:
            retList['message'] = "no available tellers"
            return Response(retList)
        for i in range(0,tellers):
            time.append(0)
        for i in tellersnotavail:
            time[i.teller_number] = 9999999
        for i in user_in_line:
            indx = numpy.argmin(time)
            if i.pk == check.pk and i.status != 'R':
                break;
            predicted = i.computed_time
            time[indx] += predicted
        indx = numpy.argmin(time)
        if time[indx] == 9999999:
            time[indx] = 0
        t = datetime.now() + timedelta(seconds=time[indx])
        t = t.strftime("%Y-%m-%dT%H:%M:%S")
        retList['time_joined'] = check.time_joined.strftime("%Y-%m-%dT%H:%M:%S")
        retList['waiting_time'] = t
        retList['priority_number'] = check.priority_num
        retList['uuid'] = uuidvar
        return Response(retList)

    @action(methods=['get'], detail=True)
    def getPriorityandWaiting(self, request, pk=None):
        check = Service.objects.filter(pk=pk).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid service'
            return Response(retList)
        user_in_line = Transaction.objects.filter(status='A', service=check).order_by('time_joined').all()
        prio = Transaction.objects.filter(status='A', service=service).order_by('time_joined').all()
        tellers = check.teller.count()
        tellersnotavail = check.teller.filter(is_active=False).all()
        time = []
        if tellersnotavail.count() == tellers:
            retList['message'] = "no available tellers"
            return Response(retList)
        for i in range(0,tellers):
            time.append(0)
        for i in tellersnotavail:
            time[i.teller_number] = 9999999
        for i in user_in_line:
            indx = numpy.argmin(time)
            predicted = i.computed_time
            time[indx] += predicted
        indx = numpy.argmin(time)
        if time[indx] == 9999999:
            time[indx] = 0
        retList['message'] = "successfully retrieved"
        t = datetime.now() + timedelta(seconds=time[indx])
        t = t.strftime("%Y-%m-%dT%H:%M:%S")
        company = check.company.service.all()
        for idx,i in enumerate(company):
            if i.service_name is check.service_name:
                priority_num = idx
        if prio.count() > 0:
            user = prio.reverse()[0]
            priority_num = int(user.priority_num.split("-",1)[1]) + 1
            priority_num = str(idx) + '-' + str(priority_num)
        else:
            priority_num = str(idx) + '-0'
        retList['waiting_time'] = t
        retList['priority_number'] = priority_num
        return Response(retList)

    @action(methods=['get'], detail=True)
    def getservice(self, request, pk=None):
        company = Company.objects.filter(pk=pk).first()
        service = Service.objects.filter(company=company)
        data = ServiceSerializer(service, many=True).data
        retList = {}
        retList['service'] = data
        return Response(retList)

    @action(methods=['get'], detail=True)
    def getscreen(self, request, pk=None):
        company = Company.objects.filter(pk=pk).first()
        data = ServiceETASerializer(company.service, many=True).data
        retList = {}
        retList['service'] = data
        return Response(retList)

    @action(methods=['post'], detail=False)
    def joinreservedqueue(self, request):
        obj = request.data
        transaction = Transaction.objects.filter(uuid=obj['uuid']).first()
        service = transaction.service
        retList = {}
        if not service:
            retList['message'] = "service does not exist"
            return Response(retList)
        computed = ComputedServiceTime.objects.filter(Service=service).first()
        std = computed.std
        drift = computed.drift
        l = []
        for i in range(0,20):
            rand = std * norm.ppf(random.uniform(0, 1))
            start = int(timedelta(hours=Transaction.objects.filter(status='CP', service=service).order_by('-time_joined').first().time_started.hour, minutes=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_started.minute, seconds=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_started.second).total_seconds())
            end = int(timedelta(hours=Transaction.objects.filter(status='CP', service=service).order_by('-time_joined').first().time_ended.hour, minutes=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_ended.minute, seconds=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_ended.second).total_seconds())
            l.append((end - start) * (e**(drift + rand)))
        predicted_waiting_time = numpy.mean(l, axis=0)
        user_in_line = Transaction.objects.filter(status='A', service=service).order_by('time_joined').all()
        prio = Transaction.objects.filter(status='A', service=service).order_by('time_joined').all()
        tellers = service.teller.filter(is_active=True).count()
        totaltellers = service.teller.filter().count()
        time = []
        tellersnotavail = service.teller.filter(is_active=False).all()
        if tellersnotavail.count() == totaltellers:
            retList['message'] = "no available tellers"
            return Response(retList)
        for i in range(0,totaltellers):
            time.append(0)
        for i in tellersnotavail:
            time[i.teller_number] = 9999999
        for i in user_in_line:
            indx = numpy.argmin(time)
            predicted = i.computed_time
            time[indx] += predicted
        indx = numpy.argmin(time)
        if time[indx] == 9999999:
            time[indx] = 0
        company = service.company.service.all()
        for idx,i in enumerate(company):
            if i.service_name is service.service_name:
                priority_num = idx
        if prio.count() > 0:
            user = prio.reverse()[0]
            priority_num = int(user.priority_num.split("-",1)[1]) + 1
            priority_num = str(idx) + '-' + str(priority_num)
        else:
            priority_num = str(idx) + '-0'
        if transaction.status == 'R':
            transaction.status = 'A'
            transaction.priority_num = priority_num
            transaction.time_joined = datetime.now()
            transaction.save()
            currentserved = Transaction.objects.filter(status='A', service=service, time_ended=None).exclude(time_started=None).order_by('-time_started').first()
            if not currentserved:
                currentserved = 'none'
            else:
                currentserved = currentserved.priority_num
            retList['message'] = 'successfully joined'
            retList['teller_no'] = ''
            retList['uuid'] = transaction.uuid
            retList['time_joined'] = transaction.time_joined
            retList['current_served'] = currentserved
            retList['service_name'] = service.service_name
            retList['service_id'] = service.pk
            retList['company_name'] = service.company.company_name
        else:
            retList['message'] = 'not eligible to join'
            return Response(retList)
        retList['message'] = "successfully lined up"
        etaTime = datetime.now() + timedelta(seconds=time[indx])
        retList['waiting_time'] = etaTime.strftime("%Y-%m-%d %H:%M:%S")
        retList['priority_number'] = priority_num
        return Response(retList)
        return Response(retList)

    @action(methods=['post'], detail=True)
    def joinqueue(self, request, pk=None):
        obj = request.data
        service = Service.objects.filter(pk=pk).first()
        print(API_KEY)
        print(API_SECRET)
        retList = {}
        if not service:
            retList['message'] = "service does not exist"
            return Response(retList)
        computed = ComputedServiceTime.objects.filter(Service=service).first()
        std = computed.std
        drift = computed.drift
        l = []
        for i in range(0,10):
            rand = std * norm.ppf(random.uniform(0, 1))
            start = Transaction.objects.filter(status='CP', service=service).order_by('-time_joined').first().time_started
            end = Transaction.objects.filter(status='CP', service=service).order_by('-time_joined').first().time_ended
            print(numpy.log(1))
            l.append((end - start).total_seconds() * (e**(drift + rand)))
        print(l)
        predicted_waiting_time = numpy.median(l, axis=0)
#        predicted_waiting_time = l[numpy.argmin(l)]
        print(predicted_waiting_time)
        user_in_line = Transaction.objects.filter(status='A', service=service).order_by('time_joined').all()
        prio = Transaction.objects.filter(status='A', service=service).order_by('time_joined').all()
        print(prio)
        tellers = service.teller.filter(is_active=True).count()
        totaltellers = service.teller.filter().count()
        time = []
        tellersnotavail = service.teller.filter(is_active=False).all()
        if tellersnotavail.count() == totaltellers:
            retList['message'] = "no available tellers"
            return Response(retList)
        for i in range(0,totaltellers):
            time.append(0)
        for i in tellersnotavail:
            time[i.teller_number] = 9999999
        for i in user_in_line:
            indx = numpy.argmin(time)
            predicted = i.computed_time
            time[indx] += predicted
        indx = numpy.argmin(time)
        if time[indx] == 9999999:
            time[indx] = 0
        company = service.company.service.all()
        for idx,i in enumerate(company):
            if i.service_name is service.service_name:
                priority_num = idx
        if prio.count() > 0:
            user = prio.reverse()[0]
            priority_num = int(user.priority_num.split("-",1)[1]) + 1
            priority_num = str(idx) + '-' + str(priority_num)
        else:
            priority_num = str(idx) + '-0'
        if ('phone_num' in obj and 'when_to_notify' in obj) and (obj['phone_num'] != ''):
            phone = obj['phone_num']
            if(int(obj['when_to_notify']) <= 0):
                when = 0
            else:
                when = int(obj['when_to_notify'])
        else:
            when = None
            phone = None
        etaTime = datetime.now() + timedelta(seconds=time[indx])
        if 'uuid' in obj:
            transaction = Transaction.objects.filter(uuid=obj['uuid']).first()
            if transaction and transaction.status == 'R':
                transaction.status = 'A'
                transaction.priority_num = priority_num
                transaction.time_joined = datetime.now()
                transaction.save()
                currentserved = Transaction.objects.filter(status='A', service=service, time_ended=None).exclude(time_started=None).order_by('-time_started').first()
                if not currentserved:
                    currentserved = 'none'
                else:
                    currentserved = currentserved.priority_num
                retList['current_served'] = currentserved
                retList['message'] = 'successfully joined'
                retList['uuid'] = transaction.uuid
                retList['time_joined'] = transaction.time_joined
                retList['service_name'] = service.service_name
                retList['service_id'] = service.pk
                retList['company_name'] = service.company.company_name
            else:
                retList['message'] = 'not eligible to join'
                return Response(retList)
        else:
            status = 'A'
            if 'linelater' in obj and obj['linelater'] == 'true':
                status = 'R'
            transaction = Transaction(status=status, service=service, computed_time=predicted_waiting_time, log=1, priority_num=priority_num, when_to_notify=when, phone_num=phone)
            transaction.save()
            retList['uuid'] = transaction.uuid
            if phone is not None:
                if status == 'A':
                    client.send_message({'from': 'noLine', 'to': phone, 'text': 'Thank you for using noLine! \n noLine Code: '+str(transaction.uuid)+'\n Estimated Time: '+etaTime.strftime("%Y-%m-%d %H:%M:%S")+'\n Priority Number: '+priority_num+'\n'})
                else:
                    client.send_message({'from': 'noLine', 'to': phone, 'text': 'Thank you for using noLine! \n noLine Code: '+str(transaction.uuid)+'+\n'})
        retList['message'] = "successfully lined up"
        retList['waiting_time'] = etaTime.strftime("%Y-%m-%d %H:%M:%S")
        retList['priority_number'] = priority_num
        print(retList)
        return Response(retList)

    @action(detail=False)
    def learn(self, request):
        service = Service.objects.filter(pk=1).first()
        last_month = datetime.today() - timedelta(days=30)
        logs = Transaction.objects.filter(time_ended__gte=last_month).all()
        start = Transaction.objects.latest('pk').time_started
        end = Transaction.objects.latest('pk').time_ended
        l = []
        l2 = []
        for i in logs:
            l.append(i.log)
        std = numpy.std(l, axis=0)
        ave = numpy.mean(l, axis=0)
        var = numpy.var(l, axis=0)
        drift = ave - (var / 2)
        service = ComputedServiceTime.objects.filter(Service=service).first()
        service.std = std
        service.var = drift
        service.save()
        for i in range(0, 10):
            rand = std * norm.ppf(random.uniform(0, 1))
            start = int(timedelta(hours=Transaction.objects.latest('pk').time_started.hour, minutes=Transaction.objects.latest('pk').time_started.minute, seconds=Transaction.objects.latest('pk').time_started.second).total_seconds())
            end = int(timedelta(hours=Transaction.objects.latest('pk').time_ended.hour, minutes=Transaction.objects.latest('pk').time_ended.minute, seconds=Transaction.objects.latest('pk').time_ended.second).total_seconds())
            l2.append((end - start) * (e**(drift + rand)))
        retList = {}
        return Response(retList)

    @action(methods=['post'], detail=False)
    def cancel(self, request):
        uuid = request.data['uuid']
        transaction = Transaction.objects.filter(uuid=uuid).first()
        retList = {}
        if transaction:
            if (transaction.status == 'A' and transaction.time_started is None) or transaction.status == 'R':
                transaction.status = 'C'
                transaction.save()
                retList['message'] = 'successfully cancelled'
            else:
                retList['message'] = 'cannot cancel'
        else:
            retList['message'] = 'transaction does not exist or UUID is wrong'
        return Response(retList)

    @action(methods=['post'], detail=False)
    def reserve(self, request):
        uuid = request.data['uuid']
        transaction = Transaction.objects.filter(uuid=uuid).first()
        retList = {}
        if transaction:
            if transaction.status == 'A':
                transaction.status = 'R'
                transaction.save()
                retList['message'] = 'successfully reserved'
            else:
                retList['message'] = 'cannot reserve'
        else:
            retList['message'] = 'transaction does not exist or UUID is wrong'
        return Response(retList)

    @action(detail=False)
    def test(self, request):
        userInQueue = Transaction.objects.filter().first()
        userInQueue.time_started = datetime.now()
        print(userInQueue.uuid)
        userInQueue.save()
        retList = {}
        retList['wow'] = "woww"
        return Response(retList)


    @action(methods=['get'], detail=True)
    def leave(self, request):
        return Response("wowow")

    @action(methods=['get'], detail=True)
    def send_feedback(self, request):
        return Response("wowow")
