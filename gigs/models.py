from django.db import models
from django.conf import settings
from accounts.models import Specialty


# Second class model because it depends on category model
modes = (
    ('created','created'),
    ('quoted','quoted'),
    ('transit','transit'),
    ('completed','completed')
)


class Request(models.Model):
    points = models.FloatField(default=10.0,help_text="This is how much points that are required to submit a quote for this request")
    date_time_created = models.DateTimeField(null=True, auto_now_add=True)
    date_created = models.DateField(null=True, auto_now_add=True)
    time_created = models.TimeField(null=True, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,help_text="Who actually created the request?")
    request_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name="request_by",help_text="The client who created this request")
    detail = models.TextField(null=True,help_text="This should say what the client wants")
    specialty = models.ForeignKey(Specialty,null=True,on_delete=models.SET_NULL,help_text="To what specialty do we classify this request")
    updated = models.BooleanField(default=False)
    time_updated = models.DateTimeField(null=True,blank=True)
    completed = models.BooleanField(default=False)
    time_completed = models.DateTimeField(null=True,blank=True)
    mode = models.CharField(max_length=20,null=True,choices=modes,default='created')

    def __str__(self):
        if self.specialty:
            return self.specialty.name
        else:
            return self.detail


# This model is for quotes that will be created
# Third class model because it depends directly on request model
class Quote(models.Model):
    request = models.ForeignKey(Request,null=True,on_delete=models.SET_NULL,related_name="quotes")
    date_time_submitted = models.DateTimeField(null=True, auto_now_add=True)
    date_submitted = models.DateField(null=True, auto_now_add=True)
    time_submitted = models.TimeField(null=True, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,help_text="Who created the quote?")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name="submitted_by",help_text="Who was this quote created for?")
    updated = models.BooleanField(default=False)
    time_updated = models.DateTimeField(null=True,blank=True)
    accepted = models.BooleanField(default=False)
    time_accepted = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return "Quote submitted for {} by {}".format(self.request,self.submitted_by.username)
