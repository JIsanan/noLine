from channels.auth import AuthMiddlewareStack
from Teller.models import Teller
from Transaction.models import Transaction


class EmployeeTellerMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query = scope['query_string'].decode()
        token_name, token_key = query.replace('%20', ' ').split()
        scope['user'] = 'does not exist'
        if token_name == 'uuid':
            token = Transaction.objects.get(uuid=token_key).first()
            if token is None:
                token = Teller.objects.get(uuid=token_key).first()
                if token is not None:
                    scope['user'] = token
            else:
                scope['user'] = token
        return self.inner(scope)


EmployeeTellerMiddlewareStack = lambda inner: EmployeeTellerMiddleware(AuthMiddlewareStack(inner))
