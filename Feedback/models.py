from django.db import models
from Service.models import Service
from Transaction.models import Transaction


class Feedback(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        related_name='feedback',
        on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service,
        related_name='feedback',
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField()
    complaint = models.TextField(max_length=500)
