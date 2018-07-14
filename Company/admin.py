from django.contrib import admin
from Company.models import Company
from Service.models import Service
from Teller.models import Teller
from Transaction.models import Transaction

# Register your models here.
admin.site.register(Company)
admin.site.register(Service)
admin.site.register(Teller)
admin.site.register(Transaction)
