# Generated by Django 4.2.1 on 2023-05-30 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optic', '0025_alter_brand_status_alter_category_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
