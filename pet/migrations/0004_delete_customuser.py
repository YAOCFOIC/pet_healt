# Generated by Django 4.2.4 on 2023-08-06 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_remove_customuser_phone_customuser_phone_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
