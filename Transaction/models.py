from django.db import models
from Service.models import Service
import uuid


class Transaction(models.Model):
    SKIPPED = 'S'
    CANCELLED = 'C'
    AVAILABLE = 'A'
    COMPLETED = 'CP'
    RESERVED = 'R'
    STATUS = (
        (SKIPPED, 'Skipped'),
        (CANCELLED, 'Cancel'),
        (AVAILABLE, 'Available'),
        (COMPLETED, 'Completed'),
        (RESERVED, 'Reserved'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=AVAILABLE,
    )
    uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    service = models.ForeignKey(
        Service,
        related_name='transaction',
        on_delete=models.CASCADE,
    )

    time_started = models.DateTimeField(null=True, blank=True)
    time_ended = models.DateTimeField(null=True, blank=True)
    computed_time = models.IntegerField()
    time_joined = models.DateTimeField(auto_now_add=True)
    priority_num = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    when_to_notify = models.PositiveIntegerField(null=True, blank=True)
    log = models.FloatField()

    def __str__(self):
        return self.uuid.__str__()
