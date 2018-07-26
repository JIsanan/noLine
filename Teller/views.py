from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from Service.models import Service
from Service.serializer import ServiceSerializer
from Teller.models import Teller
from Transaction.models import Transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import numpy as np
from datetime import datetime, date, timedelta
import pytz


class TellerViewSet(ViewSet, APIView):

    @action(methods=['post'], detail=False)
    def authenticate(self, request):
        obj = request.data
        check = Teller.objects.filter(uuid=obj['uuid']).first()
        retList = {}
        if check:
            retList['message'] = 'successfully connected'
            retList['service_name'] = check.service.service_name
            retList['service_pk'] = check.service.pk
            retList['company_name'] = check.service.company.company_name
        else:
            retList['message'] = 'incorrect'
            return Response(retList)
        if check.transaction is not None:
            retList['message'] = 'continue'
            retList['priority_num'] = check.transaction.priority_num
        userInQueue = Transaction.objects.filter(status='A', time_started=None, service=check.service).order_by('time_joined').all()
        retList['amount_of_people'] = userInQueue.count()
        check.is_active = True
        check.save()
        layer = get_channel_layer()
        telleravail = Teller.objects.filter(is_active=True, service=check.service.pk).all()
        async_to_sync(layer.group_send)('kiosk_' + str(check.service.company.pk), {
            'type': 'get.changeofonline',
            'amount': telleravail.count(),
            'servicepk': check.service.pk, 
        })
        async_to_sync(layer.group_send)('screen_' + str(check.service.company.pk), {
            'type': 'get.changeofonlinescreen',
            'is_active': 'true',
            'servicepk': check.service.pk, 
            'tellerpk': check.pk,
        })
        return Response(retList)

    @action(methods=['post'], detail=False)
    def skip(self, request):
        uuid = request.data['uuid']
        check = Teller.objects.filter(uuid=uuid).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid teller'
            return Response(retList)
        if check.is_active == False:
            retList['message'] = 'logged out'
            return Response(retList)
        if not check.transaction:
            retList['message'] = 'waiting'
            return Response(retList)
        check.availability = True
        transaction = check.transaction
        transaction.status = 'S'
        transaction.save()
        check.transaction = None
        check.save()
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('transaction_' + str(check.service.pk), {
            'type': 'get.userskipped',
            'transpk': transaction.pk,
        })                
        async_to_sync(layer.group_send)('screen_' + str(check.service.company.pk), {
            'type': 'get.changeofscreen',
            'servicepk': check.service.pk,
            'tellerpk': check.pk,
            'current': 'none',
        })
        retList['message'] = 'user has been skipped'
        return Response(retList)

    @action(methods=['post'], detail=False)
    def finish(self, request):
        uuid = request.data['uuid']
        check = Teller.objects.filter(uuid=uuid).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid teller'
            return Response(retList)
        if check.is_active == False:
            retList['message'] = 'logged out'
            return Response(retList)
        if not check.transaction:
            retList['message'] = 'waiting'
            return Response(retList)
        check.availability = True
        transaction = check.transaction
        transaction.status = 'CP'
        print("why")
        transaction.time_ended = datetime.now()
        previous = Transaction.objects.filter(status='CP', service=transaction.service).order_by('-time_joined').first()
        currentstart = transaction.time_started.replace(tzinfo=None)
        currentend = transaction.time_ended.replace(tzinfo=None)
        currentduration = (currentend - currentstart).total_seconds()
        print(previous)
        print("why")
        prevstart = previous.time_started.replace(tzinfo=None)
        print("WOW")
        prevend = previous.time_ended.replace(tzinfo=None)
        print("START")
        prevduration = (prevend - prevstart).total_seconds()
        print(currentduration)
        print(prevduration)
        transaction.log = np.log(currentduration / prevduration)
        print(transaction.log)
        transaction.save()
        check.transaction = None
        check.save()        
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('screen_' + str(check.service.company.pk), {
            'type': 'get.changeofscreen',
            'servicepk': check.service.pk,
            'tellerpk': check.pk,
            'current': 'none',
        })
        retList['message'] = 'user is done'
        return Response(retList)

    @action(methods=['post'], detail=False)
    def logout(self, request):
        uuid = request.data['uuid']
        check = Teller.objects.filter(uuid=uuid).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid teller'
            return Response(retList)
        request.user = check
        check.is_active = False
        check.save()
        layer = get_channel_layer()
        telleravail = Teller.objects.filter(is_active=True, service=check.service.pk).all()
        async_to_sync(layer.group_send)('kiosk_' + str(check.service.company.pk), {
            'type': 'get.changeofonline',
            'amount': telleravail.count(),
            'servicepk': check.service.pk, 
            'tellerpk': check.pk,
        })
        async_to_sync(layer.group_send)('screen_' + str(check.service.company.pk), {
            'type': 'get.changeofonlinescreen',
            'is_active': 'false',
            'servicepk': check.service.pk, 
            'tellerpk': check.pk,
        })
        return Response(retList)
