from django.shortcuts import render,HttpResponse
import json
from .models import *
from random import choice
from django.shortcuts import get_object_or_404
import json
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.views.decorators.csrf import csrf_exempt


def gen_token(length):
        token = ''.join([choice('ABCDEFGHIJKLMNOPQabcdefghijklmnopqrstuvwxyz0123456789') for i in range(length)])
        return token

# Utitlity classes and functions (For json parsing of objects)
class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            try:
                mypath = o.path
            except:
                return ''
            else:
                return mypath
        # this will either recusively return all atrributes of the object or return just the id
        elif isinstance(o, Model):
            return model_to_dict(o)
            # return o.id

        return super().default(o)

# Create your views here.
def index(request):
    template_name = "accounts/index.html"
    args = {}
    return render(request,template_name,args)

def check(request):
    template_name = "accounts/check-questions.html"
    args = {}
    return render(request,template_name,args)

class Activity:
    # class constructor, initializer
    # TODO: look for a better way to get these models automatically
    def __init__(self,modelName):
        self.modelName = modelName
        self.objects = {'User':CustomUser,
        'Pro':Pro,
        'Client':Client,
        'Agent':Agent,
        'Sos':SosAccount
        }

    # class method, creates instances for given models using fields
    # Goes on to add children to the model if specified
    def create(self,models,**kwargs):
        """
        This method creates instances of given modelname(s) 
        using key,val pair from fields keyword arguments. Children
        are added if a list of them are added.
        """
        results = []
        for model in models:
            instance = None
            try:
            # creating instance as django model object based on passed modelName string
                instance = self.objects[model['modelname']]()
            # This error may usually be KeyError
            except Exception as e:
                model_result = {'parent':instance,'children':[],'message':str(e)}
            else:
                for key,val in model['fields'].items():
                    try:
                        if key == "password":
                            password = make_password(val)
                            instance.__setattr__(key,password)
                        else:
                            instance.__setattr__(key,val)
                    except:
                        pass
                try:
                    instance.save()
                except Exception as e:
                    model_result = {'parent':None,'children':[],'message':str(e)}
                else:
                    children = []
                    child_instance = None
                    # Does the model have any children?
                    try:
                        model['children']
                    except Exception as e:
                        model_result = {'parent':instance,'children':[],'message':str(e)}
                    else:
                        for child in model['children']:
                            if isinstance(child['fields'], Model):
                                child_instance = child['fields']
                                try:
                                    if child['child_type'] == "many_to_many":
                                        instance.__setattr__(child['child_name'],[child_instance,])
                                    else:
                                        instance.__setattr__(child['child_name'],child_instance)
                                except:
                                    pass
                                else:
                                    instance.save()
                            # were ids given for child instances?
                            elif 'ids' in child['fields'].keys():
                                print(child['fields']['ids'])
                                # child_instance = self.objects[child['modelname']].__getattr__.get('id',child['fields']['ids'])
                                # if child['child_type'] == "many_to_many":
                                #     instance.__setattr__(child['child_name'],[child_instance,])
                                # else:
                                #     instance.__setattr__(child['child_name'],child_instance)
                                # instance.save()
                            else:
                                try:
                                    child_instance = self.objects[child['modelname']]()
                                except Exception as e:
                                    children.append(child_instance)  
                                else:
                                    for key,val in child['fields'].items():
                                        try:
                                            child_instance.__setattr__(key,val)
                                        except:
                                            pass
                                    # try saving child instance
                                    try:
                                        child_instance.save()
                                    except:
                                        pass
                                    else:
                                        try:
                                            if child['child_type'] == "many_to_many":
                                                instance.__setattr__(child['child_name'],[child_instance,])
                                            else:
                                                instance.__setattr__(child['child_name'],child_instance)
                                        except:
                                            pass
                                        else:
                                            instance.save()
                            children.append(child_instance)     
                        model_result = {'parent':instance,'children':children}
            results.append(model_result)
        return {'success':True,'message':'successful','objects':results}
        


    # reads from database the particular model instance given
    # DONE: add specific field to be returned as **fields
    def read(self,key_id,primary_key,*fields):
        """
        This method will return an object containing all
        the fields and values of the instance requested. 
        key id tell the field that represents the primary key
        and primary key is the given value for the particular instance
        we want.
        If fields are given, then only those fields with their values
        will be returned. Fields that exist on the instance model 
        but do not contain or have values will not be returned
        """
        # setting the model based on passed model string
        # and getting all fields of the model
        allfields = self.objects[self.modelName]._meta.get_fields()
        # setting instance as passed instance
        instance = self.objects[self.modelName].__getattr__.get(key_id,primary_key)
        names = []
        vals = []
        # here we get all the available fields on a particular instance
        # this means if the field is not yet created for the instance
        #  but exists on the model, 
        # it will not be taken
        objects = {}
        # This will use user defined field when returning the object requested
        if fields:
            for field in fields:
                try:
                    val = (getattr(instance, field))
                except:
                    pass
                else:
                    names.append(field)
                    try:
                        obj = list(val.values())
                    except:
                        vals.append(val)
                    else:
                        vals.append(obj)
            for i,e in enumerate(names):
                objects[e]=vals[i]

        else:
            # this will return all available fields on the instance
            for field in allfields:
                try:
                    val = (getattr(instance, field.name))
                except:
                    pass
                else:
                    names.append(field.name)
                    try:
                        obj = list(val.values())
                    except:
                        vals.append(val)
                    else:
                        vals.append(obj)
            for i,e in enumerate(names):
                objects[e]=vals[i]
            # our return dictionary contains fields with 
            # their values even ManyToMany or related field
            # Already serialized
        dump = json.dumps(objects,cls=ExtendedEncoder)
        return {'success':True,'data':dump}

    # class method to update object
    def update(self,key_id,primary_key,**kwargs):
        """
        This method will update a given model instance
        using the given key id and its value:primary key 
        """
        try:
            instance = self.objects[self.modelName].__getattr__.get(key_id,primary_key)
        except Exception as e:
            return {'success':False,'message':str(e)}
        else:
            for key,val in kwargs.items():
                try:
                    instance.__setattr__(key,val)
                except:
                    pass
                else:
                    instance.save()
            instance.save()
        return {'success':True,'message':'successfully updated'}


    # class method to delete instance of the model
    def delete(self,key_id,primary_key):
        """
        This method simply deletes the given instance primary id
        """
        try:
            instance = self.objects[self.modelName].__getattr__.get(key_id,primary_key)
        except Exception as e:
            return {'success':False,'message':str(e)}
        else:
            instance.delete()
            return {'success':True,'message':'successfully deleted'}


# function to create Sos Account for user(s)
def createSos(objects):
    users=[]
    for user in objects:
        obj = {'modelname':'Sos',
                    'fields':{'credit':0.0,
                    'momo_number':user.phone
                    },
                    'children':[
                        {'modelname':'User',
                        'child_name':'user',
                        'fields':user
                        }
                        ]
                    }
        users.append(obj)
    sos = Activity('User')
    bundle = sos.create(users)
    return bundle


# This api handles account creation for all types of users
@csrf_exempt
def createUser(request):
    """
    Example of how the structure of models to be created should look
    like after receiving all the information from the api call
    trying to create the user object.

    Below makes an example of creating 2 users with GPS child for each
    example = [
            {"modelname":"Buyer",
            "fields":{
                "username":"TheoElia",
                "password":"hellothere22",
                "momo_number":"+233203592400"
            },
            "children":[
                {
                    "modelname":"Specialty",
                    "child_name":"specialties",
                    "child_type":"many_to_many",
                    "fields":{
                        "name":"Capentry"
                    }
                }
            ]
            },
            {
                "modelname":"Seller",
                "fields":{
                    "username":"Fred",
                    "password":"Freddy234",
                    "momo_number":"+233558544343"
                },
            "children":[
                {
                    "modelname":"Specialty",
                    "child_name":"specialties",
                    "child_type":"many_to_many",
                    "fields":{
                        "name":"Painting"
                    }
                }
            ]   
            }
        ]

    """   
    json_data = json.loads(str(request.body, encoding='utf-8'))
    objects = {}
    # This for loop contructs key,val pairs
    # from incoming request body of api call
    for key,val in json_data.items():
        objects[key] = val
    activity = Activity('User')
    models=objects['models']
    # Any validation should have already been done
    execution = activity.create(models)
    # if everything went as expected
    response = {}
    if execution['success']:
        data = execution['objects']
        error = ""
        # DONE: create sos account for the user(s) as well.
        credits = []
        # compounding all user objects created
        for each in data:  
            if each['parent']:   
                user = each['parent']
                credits.append(user)
            else:
                error = each['message']
        # Did we create at least one user object? 
        # Then let's generate Sos Account for them
        if len(credits) > 0:
            bundle = createSos(credits)
            if bundle['success']: 
                credit = {'sos_accounts':bundle['objects']}
                data.append(credit)
                response['message']= "Created user account(s)"
                response['success'] = True
                # response['data']=data 
            else:
                response['message'] = "Could not create Sos accounts"
                response['success'] = True
                # response['data']=data
        else:
            response['success'] = False
            response['message'] = error
        
    else:
        response = {'success':False,'message':'User was not created'}
    dump = json.dumps(response,cls=ExtendedEncoder)
    return HttpResponse(dump, content_type='application/json')


# This api creates a new pro
# def signup_pro_api(request):
#     # colleting all field from registration of a pro
#     json_data = json.loads(str(request.body, encoding='utf-8'))
#     try:
#         username = json_data['username']
#         password = json_data['password']
#         specialties = json_data['specialties']
#         middleName = json_data['middleName']
#         firstName = json_data['firstName']
#         lastName = json_data['lastName']
#         idType = json_data['idType']
#         idNumber = json_data['idNumber']
#         email = json_data['email']
#         gender = json_data['gender']
#         region = json_data['region']
#         dob = json_data['dob']
#         free_comment = json_data['free_comment']
#         locationOfService = json_data['locationOfService']
#         address = json_data['address']
#         businessName = json_data['businessName']
#         phone = json_data['phone']
#     except Exception as e:
#         data = {'success':False,'message':str(e)}
#     else:
#         # Now initiate creating a new pro
#         try:
#             pro = Pro()
#             pro.username = username
#             pro.set_password(password)
#             pro.userType = 'Pro'
#             pro.save()
#             for each in specialties:
#                 specialty = Specialty.objects.get(name=each)
#                 pro.specialties.add(specialty)
#                 pro.save()
#             pro.first_name = firstName
#             pro.middle_name = middleName
#             pro.last_name = lastName
#             pro.id_type = idType
#             pro.id_number = idNumber
#             pro.region = region
#             pro.locationOfService = locationOfService
#             pro.address = address
#             pro.gender = gender
#             # this must be a date object
#             pro.dob = dob
#             pro.businessName = businessName
#             pro.free_comment = free_comment
#             pro.referral_token = gen_token(25)
#         except Exception as e:
#             data = {'success':False,'message':str(e)}
#         else:
#             pro.save()
#             data = {'success':True,'message':'Pro created successfully.Please verify the account.'}
#         dump = json.dumps(data)
#         return HttpResponse(dump, content_type='application/json')
#     dump = json.dumps(data)
#     return HttpResponse(dump, content_type='application/json')


# This api creates a new client
# def signup_client_api(request):
#     # colleting all field from registration of a client
#     json_data = json.loads(str(request.body, encoding='utf-8'))
#     try:
#         username = json_data['username']
#         password = json_data['password']
#         middleName = json_data['middleName']
#         firstName = json_data['firstName']
#         lastName = json_data['lastName']
#         phone = json_data['phone']
#         email = json_data['email']
#     except Exception as e:
#         data = {'success':False,'message':str(e)}
#     else:
#         try:
#             client = Client()
#             client.username = username
#             client.set_password(password)
#             client.middle_name = middleName
#             client.phone = phone
#             client.email = email
#             client.userType = 'Client'
#             client.save()
#         except Exception as e:
#             data = {'success':False,'message':str(e)}
#         else:
#             client.save()
#             data = {'success':True,'message':'Client created successfully. Please verify the account.'}
#     dump = json.dumps(data)
#     return HttpResponse(dump, content_type='application/json')