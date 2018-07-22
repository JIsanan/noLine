
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Service.models import Service
from Teller.models import Teller
import time
import json


class TellerConsumer(WebsocketConsumer):
    def connect(self):
        group = 'teller_' + str(self.scope['url_route']['kwargs']['service_id'])
        pk = int(self.scope['url_route']['kwargs']['service_id'])
        service = Service.objects.filter(pk=pk).exists()
        if service:
            async_to_sync(self.channel_layer.group_add)(
                group,
                self.channel_name
            )
            self.accept()
            jsontext = {}
            jsontext['message'] = 'successfully connected' 
            self.send(text_data=json.dumps(jsontext))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()

    def get_newcustomer(self, event):
        check = Teller.objects.filter(pk=event['tellerpk']).first()
        if check.uuid == self.scope['user'].uuid:
            self.send(text_data=json.dumps({
                'message': 'get new customer',
                'priority_num': event['priority_num'],
            }))

    def get_changeofamount(self, event):
        self.send(text_data=json.dumps({
            'message': 'change of amount',
            'amount_of_people': event['amount'],
        }))
