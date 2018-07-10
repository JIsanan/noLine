from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from Service.models import Service
from Service.serializer import ServiceSerializer
from Teller.models import Teller

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class TransactionViewSet(ViewSet, APIView):

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
    def leave(self, request):

    @action(methods=['get'], detail=True)
    def send_feedback(self, request):