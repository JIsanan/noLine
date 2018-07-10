from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from Service.models import Service
from Service.serializer import ServiceSerializer
from Teller.models import Teller

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class TellerViewSet(ViewSet, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def authenticate(self, request):
        obj = request.data
        check = Teller.objects.filter(uuid=obj['uuid']).exists()
        retList = {}
        if check:
            retList['message'] = 'successfully connected'
        else:
            retList['message'] = 'incorrect'
        return Response(retList)

    @action(methods=['get'], detail=True)
    def skip(self, request):
        uuid = request.META.get('AUTHORIZATION')
        check = Teller.objects.filter(uuid=uuid).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid teller'
            return Response(retList)
        request.user = check
        return Response(retList)

    @action(methods=['get'], detail=True)
    def finish(self, request):
        uuid = request.META.get('AUTHORIZATION')
        check = Teller.objects.filter(uuid=uuid).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid teller'
            return Response(retList)
        request.user = check
        return Response(retList)

    @action(methods=['get'], detail=True)
    def logout(self, request):
        uuid = request.META.get('AUTHORIZATION')
        check = Teller.objects.filter(uuid=uuid).first()
        retList = {}
        if not check:
            retList['message'] = 'not a valid teller'
            return Response(retList)
        request.user = check
        return Response(retList)
