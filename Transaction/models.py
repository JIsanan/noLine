from django.db import models
from Employee.models import Employee
from Service.models import Service
import uuid


class Transaction(models.Model):
    uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    employee = models.ForeignKey(
        Employee,
        related_name='transaction',
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        related_name='transaction',
        on_delete=models.CASCADE,
    )
    time_started = models.DateTimeField(null=True)
    time_ended = models.DateTimeField(null=True)
    computed_time = models.IntegerField()
    time_joined = models.DateTimeField(auto_now_add=True)
    priority_num = models.CharField(max_length=20)
