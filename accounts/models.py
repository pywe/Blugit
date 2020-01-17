from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django_mysql.models import ListTextField


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    is_staff = models.BooleanField(default=False)
    


# Pro model:migrates into database as accounts_pro table
class Pro(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Pro"

# Client model:migrates into database as accounts_client table
class Client(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Client"


# Agent model:migrates into database as accounts_agent table
class Agent(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Agent"