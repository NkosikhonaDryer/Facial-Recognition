# Generated by Django 4.1.7 on 2023-10-10 21:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_rename_student_themdes_studentid_themdes_studentname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='themdes',
            name='type',
            field=models.CharField(default='success', max_length=20),
        ),
        migrations.AlterField(
            model_name='class',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 10, 23, 14, 44, 346408)),
        ),
        migrations.AlterField(
            model_name='group',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 10, 23, 14, 44, 346408)),
        ),
        migrations.AlterField(
            model_name='module',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 10, 23, 14, 44, 346408)),
        ),
        migrations.AlterField(
            model_name='program',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 10, 23, 14, 44, 346408)),
        ),
    ]