# Generated by Django 2.2.10 on 2020-04-09 04:40

from django.db import migrations
import helios_auth.jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('helios', '0014_auto_20200406_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='voters_who_voted_json',
            field=helios_auth.jsonfield.JSONField(null=True),
        ),
    ]
