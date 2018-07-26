from rest_framework import serializers
from Service.models import Service
from Company.serializers import CompanySerializer
from Transaction.models import Transaction
from Teller.models import Teller

from datetime import datetime, date, timedelta

import numpy


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer(read_only=True, many=False,)
    online_tellers = serializers.SerializerMethodField()
    people_in_line = serializers.SerializerMethodField()
    eta = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'service_name', 'company', 'pk', 'online_tellers', 'people_in_line', 'eta')

    def get_online_tellers(self, obj):
    	return obj.teller.filter(is_active=True).count()

    def get_people_in_line(self, obj):
    	return Transaction.objects.filter(status='A', time_started=None, service=obj).order_by('time_joined').count()

    def get_eta(self, obj):
        check = obj
        user_in_line = Transaction.objects.filter(status='A', time_started=None, service=check).order_by('time_joined').all()
        tellers = check.teller.count()
        tellersnotavail = check.teller.filter(is_active=False).all()
        time = []
        if tellersnotavail.count() == tellers:
        	return ''
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
        t = datetime.now() + timedelta(seconds=time[indx])
        t = t.strftime("%Y-%m-%dT%H:%M:%S")
        return t

class TellerETASerializer(serializers.HyperlinkedModelSerializer):
    current = serializers.SerializerMethodField()

    class Meta:
        model = Teller
        fields = (
            'pk', 'current', 'is_active')

    def get_current(self, obj):
    	if obj.transaction:
    		return obj.transaction.priority_num
    	else:
    		return 'none'


class ServiceETASerializer(serializers.HyperlinkedModelSerializer):
    teller = TellerETASerializer(read_only=True, many=True,)

    class Meta:
        model = Service
        fields = (
            'service_name', 'pk', 'teller',)
