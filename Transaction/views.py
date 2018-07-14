from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from Service.models import Service
from Service.serializer import ServiceSerializer
from Teller.models import Teller
from Company.models import Company
from Transaction.models import Transaction
from ComputedServiceTime.models import ComputedServiceTime

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from datetime import datetime, date, time, timedelta
from scipy.stats import norm
from math import e
import random
import numpy


class TransactionViewSet(ViewSet, APIView):

	def list(self, request):
		return Response("none")

	@action(methods=['post'], detail=True)
	def authenticate(self, request):
		uuid = request.META.get('AUTHORIZATION')
		check = Transaction.objects.filter(uuid=uuid).first()
		retList = {}
		if not check:
			retList['message'] = 'not a valid customer'
			return Response(retList)
		request.user = check
		return Response(retList)

	@action(methods=['get'], detail=True)
	def getservice(self, request, pk=None):
		company = Company.objects.filter(pk=pk).first()
		service = Service.objects.filter(company=company).all()
		data = ServiceSerializer(service, many=True).data
		retList = {}
		retList['service'] = data
		return Response(retList)

	@action(methods=['get'], detail=True)
	def joinqueue(self, request, pk=None):
		service = Service.objects.filter(pk=pk).first()
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
			start = int(timedelta(hours=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_started.hour, minutes=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_started.minute, seconds=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_started.second).total_seconds())
			end = int(timedelta(hours=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_ended.hour, minutes=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_ended.minute, seconds=Transaction.objects.filter(status='CP').order_by('-time_joined').first().time_ended.second).total_seconds())
			l.append((end - start) * (e**(drift + rand)))
		predicted_waiting_time = numpy.mean(l, axis=0)

		user_in_line = Transaction.objects.filter(status='A').order_by('time_joined').all()
		tellers = service.teller.filter(is_active=True).count()
		time = []
		if tellers <= 0:
			retList['message'] = "no available tellers"
			return Response(retList)
		for i in range(0,tellers):
			time.append(0)
		for i in user_in_line:
			indx = numpy.argmin(time)
			predicted = i.computed_time
			time[indx] += predicted
		indx = numpy.argmin(time)
		company = service.company.service.all()
		for idx,i in enumerate(company):
			if i.service_name is service.service_name:
				priority_num = idx
		user = user_in_line.reverse()[0]
		priority_num = int(user.priority_num.split("-",1)[1]) + 1
		priority_num = str(idx) + '-' + str(priority_num)
		transaction = Transaction(service=service, computed_time=predicted_waiting_time, log=1, priority_num=priority_num)
		transaction.save()
		retList['message'] = "successfully lined up"
		retList['waiting_time'] = time[indx]
		retList['priority_number'] = priority_num
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
		drift = ave - (var/2)
		service = ComputedServiceTime.objects.filter(Service=service).first()
		service.std = std
		service.var = drift
		service.save()
		for i in range(0,10):
			rand = std * norm.ppf(random.uniform(0, 1))
			start = int(timedelta(hours=Transaction.objects.latest('pk').time_started.hour, minutes=Transaction.objects.latest('pk').time_started.minute, seconds=Transaction.objects.latest('pk').time_started.second).total_seconds())
			end = int(timedelta(hours=Transaction.objects.latest('pk').time_ended.hour, minutes=Transaction.objects.latest('pk').time_ended.minute, seconds=Transaction.objects.latest('pk').time_ended.second).total_seconds())
			l2.append((end - start) * (e**(drift + rand)))
		retList = {}
		return Response(retList)

	@action(methods=['get'], detail=True)
	def leave(self, request):
		return Response("wowow")

	@action(methods=['get'], detail=True)
	def send_feedback(self, request):
		return Response("wowow")