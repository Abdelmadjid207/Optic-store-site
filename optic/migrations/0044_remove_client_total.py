# Generated by Django 4.2.1 on 2023-06-22 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('optic', '0043_cart_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='total',
        ),
    ]
