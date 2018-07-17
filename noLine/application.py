from channels.routing import ProtocolTypeRouter, URLRouter
from noLine.employee_teller_auth import EmployeeTellerMiddlewareStack
from django.urls import path
from teller.consumers import TellerConsumer
from transaction.consumers import TransactionConsumer

application = ProtocolTypeRouter({
    'websocket': EmployeeTellerMiddlewareStack(
        URLRouter([
            path('ws/teller/<int:service_id>/', TellerConsumer),
            path('ws/customer/<int:service_id>', TransactionConsumer),
        ])
    ),
})
