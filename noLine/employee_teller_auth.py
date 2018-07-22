from channels.auth import AuthMiddlewareStack
from Teller.models import Teller
from Transaction.models import Transaction
from Company.models import Company

from django.contrib.auth.models import AnonymousUser


class EmployeeTellerMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query = scope['query_string'].decode()
        token_name, token_key = query.replace('%20', ' ').split()
        scope['user'] = AnonymousUser()
        if token_name == 'uuid=uuid':
            token = Transaction.objects.filter(uuid=token_key).first()
            if not token:
                token = Teller.objects.filter(uuid=token_key).first()
                if token:
                    scope['user'] = token
                else:
                    scope['user'] = 'no user'
            else:
                scope['user'] = token
        if token_name == 'pk=pk':
            token = Company.objects.filter(pk=token_key).first()
            if token:
                scope['user'] = token
            else:
                scope['user'] = 'no user'
        return self.inner(scope)


EmployeeTellerMiddlewareStack = lambda inner: EmployeeTellerMiddleware(AuthMiddlewareStack(inner))
