from django.db import models
from Employee.models import Employee
from Service.models import Service
import uuid


class Teller(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='teller',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=False)
    availability = models.BooleanField(default=False)
    uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
