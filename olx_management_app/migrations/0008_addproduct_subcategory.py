# Generated by Django 4.2.4 on 2023-12-30 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx_management_app', '0007_chatmessagedata_is_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproduct',
            name='subcategory',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
