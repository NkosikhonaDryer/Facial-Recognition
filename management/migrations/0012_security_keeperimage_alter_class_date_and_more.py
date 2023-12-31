# Generated by Django 4.1.7 on 2023-10-22 15:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_alter_class_date_alter_group_datecreated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='security',
            name='Keeperimage',
            field=models.FileField(blank=True, null=True, upload_to='streamApp/images'),
        ),
        migrations.AlterField(
            model_name='class',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 17, 46, 6, 747493)),
        ),
        migrations.AlterField(
            model_name='compusattendee',
            name='dateTimeCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 17, 46, 6, 747493)),
        ),
        migrations.AlterField(
            model_name='compusattendee',
            name='datecreated',
            field=models.DateField(default=datetime.date(2023, 10, 22)),
        ),
        migrations.AlterField(
            model_name='group',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 17, 46, 6, 747493)),
        ),
        migrations.AlterField(
            model_name='module',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 17, 46, 6, 747493)),
        ),
        migrations.AlterField(
            model_name='program',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 17, 46, 6, 747493)),
        ),
        migrations.AlterField(
            model_name='security',
            name='datecreated',
            field=models.DateField(default=datetime.datetime(2023, 10, 22, 17, 46, 6, 747493)),
        ),
    ]
