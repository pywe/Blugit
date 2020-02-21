from django.shortcuts import render,HttpResponse
import json
from .models import *
from random import choice


def gen_token(length):
        token = ''.join([choice('ABCDEFGHIJKLMNOPQabcdefghijklmnopqrstuvwxyz0123456789') for i in range(length)])
        return token

# Create your views here.
def index(request):
    template_name = "accounts/index.html"
    args = {}
    return render(request,template_name,args)


# This api creates a new pro
def signup_pro_api(request):
    # colleting all field from registration of a pro
    json_data = json.loads(str(request.body, encoding='utf-8'))
    try:
        username = json_data['username']
        password = json_data['password']
        middleName = json_data['middleName']
        firstName = json_data['firstName']
        lastName = json_data['lastName']
        idType = json_data['idType']
        idNumber = json_data['idNumber']
        email = json_data['email']
        gender = json_data['gender']
        region = json_data['region']
        dob = json_data['dob']
        free_comment = json_data['free_comment']
        locationOfService = json_data['locationOfService']
        address = json_data['address']
        businessName = json_data['businessName']
        phone = json_data['phone']
    except Exception as e:
        data = {'success':False,'message':str(e)}
    else:
        # Now initiate creating a new pro
        try:
            pro = Pro()
            pro.username = username
            pro.set_password(password)
            pro.first_name = firstName
            pro.middle_name = middleName
            pro.last_name = lastName
            pro.id_type = idType
            pro.id_number = idNumber
            pro.region = region
            pro.locationOfService = locationOfService
            pro.address = address
            pro.gender = gender
            # this must be a date object
            pro.dob = dob
            pro.businessName = businessName
            pro.free_comment = free_comment
            pro.referral_token = gen_token(25)
        except Exception as e:
            data = {'success':False,'message':str(e)}
        else:
            pro.save()
            data = {'success':True,'message':'Pro created successfully'}
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

