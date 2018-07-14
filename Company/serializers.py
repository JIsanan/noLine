from rest_framework import serializers
from django.contrib.auth.models import User
from Company.models import Company

from rest_framework.authtoken.models import Token


class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'token')

    def get_token(self, obj):
        ret = Token.objects.filter(user=obj).all().values('key')
        return ret


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False,)

    class Meta:
        model = Company
        fields = (
            'company_name', 'user')
