from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django_mysql.models import ListTextField



class Specialty(models.Model):
    name = models.CharField(max_length=50,null=True)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name

usertypes = (
    ('Admin','Admin'),
    ('Pro','Pro'),
    ('Agent','Agent'),
    ('Client','Client')
)


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    phone = models.CharField(max_length=14,null=True,blank=True)
    userImage = models.ImageField(upload_to="static/profiles",null=True,blank=True)
    middle_name = models.CharField(max_length=50,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    userType = models.CharField(max_length=20,null=True,choices=usertypes,default="Pro")
    points = models.FloatField(default=0.0)
    


# Pro model:migrates into database as accounts_pro table
class Pro(CustomUser):
    specialties = models.ManyToManyField(Specialty)
    businessName = models.CharField(max_length=50,null=True)
    scannedId = models.FileField(upload_to="static/ids",null=True)
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
        

# Second class model
class SosAccount(models.Model):
    credit = models.FloatField(default=0.0)
    momo_number = models.CharField(max_length=14,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name='sos_account')

    class Meta:
        verbose_name = "Sos Account"

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return self.momo_number