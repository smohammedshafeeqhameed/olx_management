# Generated by Django 4.2.4 on 2023-12-30 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx_management_app', '0006_chatmessagedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessagedata',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
