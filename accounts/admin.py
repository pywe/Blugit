from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(CustomUser)
admin.site.register(Pro)
admin.site.register(Specialty)

