# Generated by Django 2.0.7 on 2018-07-14 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ComputedServiceTime', '0002_auto_20180714_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computedservicetime',
            name='ave',
        ),
        migrations.RemoveField(
            model_name='computedservicetime',
            name='var',
        ),
    ]
