# Generated by Django 4.0.6 on 2022-09-19 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LoginManager', '0002_account_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_staff',
        ),
    ]
