from django.test import TestCase
from Teller.models import Teller
from Service.models import Service
from Company.models import Company
from django.conf import settings
from django.contrib.auth.models import User


class TestTeller(TestCase):

    def setUp(self):
        user =  User.objects.create(username='hello', password='oled')
        company = Company.objects.create(company_name='Company', user=user)
        self.service = Service.objects.create(company=company, service_name='company')
        self.teller = Teller.objects.create(service=self.service)

    def test1(self):
        uuid = 'f04dd04f-3e58-4f13-b969-5a02c896a02a'
        self.assertNotEqual(uuid, self.teller.uuid)

    def test2(self):
        self.assertEqual(self.service, self.teller.service)
