from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django_mysql.models import ListTextField



class Specialty(models.Model):
    name = models.CharField(max_length=50,null=True)


    def __str__(self):
        return self.name

# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    phone = models.CharField(max_length=14,null=True)
    userImage = models.ImageField(upload_to="static/profiles",null=True)
    middle_name = models.CharField(max_length=50,null=True)
    is_staff = models.BooleanField(default=False)
    


# Pro model:migrates into database as accounts_pro table
class Pro(CustomUser):
    specialties = models.ManyToManyField(Specialty)
    businessName = models.CharField(max_length=50,null=True)
    scannedId = models.FileField(upload_to="static/IDS",null=True)
    region = models.CharField(max_length=50,null=True)
    locationOfService = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=120,null=True)
    id_type = models.CharField(max_length=20,null=True)
    id_number = models.CharField(max_length=20,null=True)
    free_comment = models.TextField(null=True)
    dob = models.DateField(null=True)
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