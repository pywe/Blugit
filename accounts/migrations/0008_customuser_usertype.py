# Generated by Django 2.2.3 on 2020-03-01 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200301_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='userType',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Pro', 'Pro'), ('Agent', 'Agent'), ('Client', 'Client')], default='Pro', max_length=20, null=True),
        ),
    ]
