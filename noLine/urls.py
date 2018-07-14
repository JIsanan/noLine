"""noLine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from Company import views as company_views
from Service import views as service_views
from Transaction import views as transaction_views
from Teller import views as teller_views


router = routers.DefaultRouter()
router.register(
    r'register', company_views.RegisterViewSet, base_name="register")
router.register(
    r'login', company_views.LoginViewSet, base_name="login")
router.register(
    r'getloggedin', company_views.CompanyViewSet, base_name="getloggedin")
router.register(
    r'service', service_views.ServiceViewSet, base_name="service")
router.register(
    r'transaction', transaction_views.TransactionViewSet, base_name="teller")
router.register(
    r'teller', teller_views.TellerViewSet, base_name="teller")

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
