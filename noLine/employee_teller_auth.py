from channels.auth import AuthMiddlewareStack
from Teller.models import Teller
from Transaction.models import Transaction

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
            token = Transaction.objects.get(uuid=token_key)
            if not token:
                token = Teller.objects.get(uuid=token_key)
                if not token:
                    scope['user'] = token
            else:
                scope['user'] = token
        return self.inner(scope)


EmployeeTellerMiddlewareStack = lambda inner: EmployeeTellerMiddleware(AuthMiddlewareStack(inner))
