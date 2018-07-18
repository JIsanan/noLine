from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from Service.models import Service
from Service.serializer import ServiceSerializer
from Teller.models import Teller
from Transaction.models import Transaction
from ComputedServiceTime.models import ComputedServiceTime

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime, timedelta


class ServiceViewSet(ViewSet, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        obj = request.data
        retdict = {}
        check = Service.objects.filter(service_name=obj['service_name'],
                                       company=request.user.company)
        if not check and int(obj['teller_count']) > 0:
            service = Service(service_name=obj['service_name'],
                              company=request.user.company)
            service.save()
            tellerlist = []
            for i in range(int(obj['teller_count'])):
                tellerlist.append(Teller(service=service, teller_number=i))
            now = datetime.now()
            end = datetime.now() + timedelta(seconds=int(obj['initial_time']))
            trans = Transaction(service=service, computed_time=0, time_started=now,time_ended=end,priority_num='0-0', log=1, status='CP')
            computed_time = ComputedServiceTime(std=0, drift=0, Service=service)
            computed_time.save()
            trans.save()
            Teller.objects.bulk_create(tellerlist)
            service = ServiceSerializer(service).data
            retdict['data'] = service
            retdict['message'] = "Service successfully created"
        else:
            retdict['message'] = "Service already exists or teller count is invalid"
        return Response(retdict)

    def list(self, request):
        queryset = Service.objects.filter(company=request.user.company).all()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Service.objects.filter(company=request.user.company, pk=pk).first()
        serializer = ServiceSerializer(queryset)
        return Response(serializer.data)
