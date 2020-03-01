from django.shortcuts import render,HttpResponse
import json
from .models import *
from accounts.models import CustomUser,Specialty
from random import choice



# This api creates a new request
def create_request(request):
    # colleting all fields from request creation
    json_data = json.loads(str(request.body, encoding='utf-8'))
    try:
        created_by = json_data['created_by']
        request_by = json_data['request_by']
        detail = json_data['detail']
        specialty = json_data['specialty']
    except Exception as e:
        data = {'success':False,'message':str(e)}
    else:
        # initial checks tuened out fine
        try:
            request = Request()
            request.detail = detail
            creator = CustomUser.objects.get(username=created_by)
            requester = CustomUser.objects.get(username=request_by)
            req_specialty = Specialty.objects.get(name=specialty)
            request.created_by = creator
            request.request_by = requester
            request.specialty = req_specialty
        except Exception as e:
            data = {'success':False,'message':str(e)}
        else:
            # if everything turned out fine
            request.save()
            data = {'success':True,'message':"Your request has been received, Please wait for Pros."}
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


# This api creates a new quote for a request
def create_quote(request):
    # colleting all fields from quote submission
    json_data = json.loads(str(request.body, encoding='utf-8'))
    try:
        created_by = json_data['created_by']
        submitted_by = json_data['submitted_by']
        request_id = json_data['request_id']
    except Exception as e:
        data = {'success':False,'message':str(e)}
    else:
        # initial checks tuened out fine
        try:
            quote = Quote()
            creator = CustomUser.objects.get(username=created_by)
            # TODO: we need to check if creator is authorised to submit quotes

            # we need to check that quoter has enough points to submit a quote
            real_request = Request.objects.get(id=int(request_id))
            quoter = CustomUser.objects.get(username=submitted_by)
            if quoter.points > real_request.points:
                quote.created_by = creator
                quote.submitted_by = quoter
                quote.request = real_request
            else:
                data = {'success':False,'message':"You do not have enough points to submit quote"}
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
        except Exception as e:
            data = {'success':False,'message':str(e)}
        else:
            # if everything turned out fine
            quote.save()
            data = {'success':True,'message':"Quote successfully submitted"}
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')