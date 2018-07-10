from rest_framework import serializers
from Service.models import Service
from Company.serializers import CompanySerializer


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer(read_only=True, many=False,)

    class Meta:
        model = Service
        fields = (
            'service_name', 'company')
