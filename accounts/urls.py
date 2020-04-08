from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index,name="home"), 
    url(r'^create-user/$', views.createUser,name="create-user"), 
    url(r'^check-questions/$', views.check,name="check-questions"), 
    ]