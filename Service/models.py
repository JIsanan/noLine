from django.db import models
from Company.models import Company


# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=128)
    company = models.ForeignKey(
        Company,
        related_name='service',
        on_delete=models.CASCADE,
    )
