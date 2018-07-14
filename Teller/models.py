from django.db import models
from Service.models import Service
from Transaction.models import Transaction
import uuid


class Teller(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='teller',
        on_delete=models.CASCADE,
    )
    transaction = models.ForeignKey(
        Transaction,
        related_name='teller',
        on_delete=models.CASCADE,
        null=True,
    )
    is_active = models.BooleanField(default=False)
    availability = models.BooleanField(default=False)
    uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
