# Generated by Django 4.2 on 2023-05-19 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optic', '0020_alter_client_added_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
