from django.db import models
from Company.models import Company
from django.conf import settings


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='employee',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='uploads/profile_pic/', 
    						  default='uploads/profile_pic/default.png',
    						  blank=True)
    company = models.ForeignKey(
        Company,
        related_name='employee',
        on_delete=models.CASCADE,
    )
