
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Service.models import Service
from Transaction.models import Transaction
import time
import json


class TransactionConsumer(WebsocketConsumer):
    def connect(self):
        service = self.scope['url_route']['kwargs']['service_id']
        group = 'transaction_' + str(self.scope['url_route']['kwargs']['service_id'])
        service = Service.objects.filter(pk=service).first()
        servicetype = 'transaction_' + str(self.scope['url_route']['kwargs']['type'])
        self.room_group_name = group
        if service:
            if servicetype is 0:
                service = service.company.pk
                group = 'kiosk_' + service
            async_to_sync(self.channel_layer.group_add)(
                group,
                self.channel_name
            )
            self.accept()
            jsontext = {}
            jsontext['text'] = 'successfully connected'
            self.send(text_data=json.dumps(jsontext))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()

    def get_changeofline(self, event):
        check = Service.objects.filter(pk=event['servicepk']).first()
        if check:
            self.send(text_data=json.dumps({
                'service_pk': event['servicepk'],
                'numberofpeople': event['servicecount'],
            }))

    def get_changeofeta(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).first()
        if user.uuid == self.scope['user'].uuid:
            self.send(text_data=json.dumps({
                'newETA': event['eta'],
                'currentserved': event['priority_num'],
            }))

    def get_usersturn(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).first()
        if user.uuid == self.scope['user'].uuid:
            self.send(text_data=json.dumps({
                'newETA': "it's the user's turn",
                'teller': event['teller_no']
            }))
