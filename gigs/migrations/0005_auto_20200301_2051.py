# Generated by Django 2.2.3 on 2020-03-01 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0004_auto_20200301_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='date_created',
            new_name='date_submitted',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='date_time_created',
            new_name='date_time_submitted',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='time_created',
            new_name='time_submitted',
        ),
    ]
