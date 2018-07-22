from rest_framework import serializers
from Service.models import Service
from Company.serializers import CompanySerializer
from Transaction.models import Transaction


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer(read_only=True, many=False,)
    online_tellers = serializers.SerializerMethodField()
    people_in_line = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'service_name', 'company', 'pk', 'online_tellers', 'people_in_line')

    def get_online_tellers(self, obj):
    	return obj.teller.filter(is_active=True).count()

    def get_people_in_line(self, obj):
    	return Transaction.objects.filter(status='A', time_started=None, service=obj).order_by('time_joined').count()