from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from django.contrib.auth.models import User
from Company.models import Company
from django.contrib.auth import authenticate
from Company.serializers import CompanySerializer
from Company.serializers import RegisterUserSerializer
from Company.serializers import UserSerializer
from Company.serializers import LoginSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RegisterViewSet(ViewSet, APIView):

    def create(self, request):
        obj = request.data
        retdict = {}
        print(obj)
        x = RegisterUserSerializer(data=obj)
        if x.is_valid() is True:
            if request.data['company_name']:
                name = request.data['company_name']
                if len(name) != 0 and len(name) < 50:
                    check = User.objects.filter(username=request.data['username']).exists()
                    if not check:
                        res = x.save()
                        company = Company(user=res, company_name=name)
                        company.save()
                        company = CompanySerializer(company).data
                        retdict['company'] = company
                        retdict['message'] = 'Successful'
                    else:
                        retdict['message'] = 'Username taken already'
                else:
                    retdict['message'] = 'Company Name has an empty string or has more than 50 characters'
            else:
                retdict['message'] = 'Company Name was not sent'
        else:
            print(x.errors)
            retdict['message'] = 'Invalid User input'
        return Response(retdict)


class LoginViewSet(ViewSet, APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        obj = request.data
        retdict = {}
        user = authenticate(username=obj['username'],
                            password=obj['password'])
        retdict['message'] = 'incorrect credentials'
        if user is not None:
            retdict['data'] = LoginSerializer(user).data
            retdict['message'] = 'log in successful'
        return Response(retdict)

class CompanyViewSet(ViewSet, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        retdict = {}
        retdict['user'] = CompanySerializer(request.user.company).data
        retdict['message'] = 'successfully retrieved'
        return Response(retdict)
