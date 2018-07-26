
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Service.models import Service
from Company.models import Company
from Transaction.models import Transaction
import time
import json


class TransactionConsumer(WebsocketConsumer):
    def connect(self):
        pk = self.scope['url_route']['kwargs']['service_id']
        group = 'transaction_' + str(self.scope['url_route']['kwargs']['service_id'])
        service = Service.objects.filter(pk=pk).first()
        servicetype = 'transaction_' + str(self.scope['url_route']['kwargs']['type'])
        self.room_group_name = group
        jsontext = {}
        if service:                
            async_to_sync(self.channel_layer.group_add)(
                group,
                self.channel_name
            )
            self.accept()
            jsontext['new_eta'] = ''
            jsontext['current_served'] = ''
            jsontext['teller'] = ''
            jsontext['message'] = 'successfully connected'
            self.send(text_data=json.dumps(jsontext))
        elif not servicetype == 'transaction_0':
            company = Company.objects.filter(pk=pk).first()
            if company:
                if servicetype == 'transaction_1':
                    group = 'kiosk_' + str(pk)
                elif servicetype == 'transaction_2':
                    group = 'screen_' + str(pk)
                async_to_sync(self.channel_layer.group_add)(
                    group,
                    self.channel_name
                )
                self.accept()
                jsontext['new_eta'] = ''
                jsontext['current_served'] = ''
                jsontext['group'] = group
                jsontext['teller'] = ''
                jsontext['message'] = 'successfully connected'
                self.send(text_data=json.dumps(jsontext))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()

    def get_changeofline(self, event):
        check = Service.objects.filter(pk=event['servicepk']).first()
        if check.company.pk == self.scope['user'].pk:
            self.send(text_data=json.dumps({
                'service_pk': str(event['servicepk']),
                'number_of_people': str(event['amount']),
                'eta': str(event['eta']),
                'message': 'line change',
            }))

    def get_changeofonline(self, event):
        check = Service.objects.filter(pk=event['servicepk']).first()
        if check.company.pk == self.scope['user'].pk:
            self.send(text_data=json.dumps({
                'service_pk': str(event['servicepk']),
                'number_of_people': str(event['amount']),
                'message': 'teller change',
            }))

    def get_changeofscreen(self, event):
        self.send(text_data=json.dumps({
            'service_pk': str(event['servicepk']),
            'current_served': event['current'],
            'teller_pk': event['tellerpk'],
            'message': 'current served change',
        }))

    def get_changeofonlinescreen(self, event):
        self.send(text_data=json.dumps({
            'service_pk': event['servicepk'],
            'is_active': str(event['is_active']),
            'teller_pk': event['tellerpk'],
            'message': 'teller online change',
        }))

    def get_changeofeta(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).first()
        if user.uuid == self.scope['user'].uuid:
            self.send(text_data=json.dumps({
                'new_eta': str(event['eta']),
                'current_served': str(event['priority_num']),
                'message': "eta change",
                'teller': "",
            }))

    def get_usersturn(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).first()
        if user.uuid == self.scope['user'].uuid:
            self.send(text_data=json.dumps({
                'new_eta': "",
                'current_served': "",
                'message': "user turn",
                'teller': str(event['teller_no']),
            }))

    def get_userskipped(self, event):
        user = Transaction.objects.filter(pk=event['transpk']).first()
        if user.uuid == self.scope['user'].uuid:
            self.send(text_data=json.dumps({
                'new_eta': "",
                'current_served': "",
                'teller': "",
                'message': "user skip",
            }))
