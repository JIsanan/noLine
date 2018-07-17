
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Service.models import Service
from Transaction.models import Transaction
import time
import json


class TransactionConsumer(WebsocketConsumer):
    def connect(self):
        service = Service.objects.filter(pk=group).first()
        if service:
            if self.scope['user'] is not 'does not exist':
                group = 'transaction_' + self.scope['url_route']['kwargs']['service_id']
            else:
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
        check = Service.objects.filter(pk=event['servicepk']).exists()
        if check:
            self.send(text_data=json.dumps({
                'service_pk': event['servicepk'],
                'numberofpeople': event['servicecount'],
            }))

    def get_changeOfETA(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).exists()
        if user:
            self.send(text_data=json.dumps({
                'newETA': event['eta'],
            }))

    def get_usersTurn(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).exists()
        if user:
            self.send(text_data=json.dumps({
                'newETA': "it's the user's turn",
            }))
