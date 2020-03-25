# Generated by Django 2.2.10 on 2020-03-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helios', '0004_auto_20200325_0744'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='election_pubkey_added_to_contract',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='election',
            name='questions_added_to_contract',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='election',
            name='voters_added_to_contract',
            field=models.IntegerField(default=0),
        ),
    ]