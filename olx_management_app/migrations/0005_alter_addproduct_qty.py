# Generated by Django 4.2.4 on 2023-12-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx_management_app', '0004_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproduct',
            name='qty',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]