from django.db import models
from Employee.models import Employee
from Service.models import Service


class Teller(models.Model):
    employee = models.OneToOneField(
        Employee,
        related_name='teller',
        null=True,
        on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service,
        related_name='teller',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=False)
    availability = models.BooleanField(default=False)
    passcode = models.CharField(max_length=64)
