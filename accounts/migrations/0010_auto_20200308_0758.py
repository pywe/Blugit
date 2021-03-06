# Generated by Django 2.2.3 on 2020-03-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200301_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='userImage',
            field=models.ImageField(blank=True, null=True, upload_to='static/profiles'),
        ),
        migrations.AlterField(
            model_name='pro',
            name='scannedId',
            field=models.FileField(null=True, upload_to='static/ids'),
        ),
    ]
