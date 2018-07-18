from django.db import models
from Service.models import Service


class ComputedServiceTime(models.Model):
    Service = models.ForeignKey(
        Service,
        related_name='computed_time',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    std = models.FloatField()
    drift = models.FloatField()
