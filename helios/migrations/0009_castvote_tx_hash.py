# Generated by Django 2.2.10 on 2020-04-06 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helios', '0008_auto_20200328_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='castvote',
            name='tx_hash',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
