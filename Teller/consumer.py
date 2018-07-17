
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Service.models import Service
from Teller.models import Teller
import time
import json


class TellerConsumer(WebsocketConsumer):
    def connect(self):
        group = 'teller_' + self.scope['url_route']['kwargs']['service_id']
        service = Service.objects.filter(pk=group).exists()
        if service:
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

    def get_newcustomer(self, event):
        check = Teller.objects.filter(pk=event['tellerpk']).exists()
        if check:
            self.send(text_data=json.dumps({
                'priority_num': event['priority_num'],
                'pk': event['pk'],
            }))
