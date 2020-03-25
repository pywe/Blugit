from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^gigs/create-request/$', views.create_request,name="create-request"), 
    url(r'^gigs/submit-quote/$', views.create_quote,name="create-quote"), 
    url(r'^gigs/accept-quote/$', views.accept_quote,name="accept-quote"), 
    ]