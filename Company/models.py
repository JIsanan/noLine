from django.db import models
from django.conf import settings


class Company(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='company',
        on_delete=models.CASCADE)
    company_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
