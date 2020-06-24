from django.conf.urls import url,include
from django.contrib import admin
from .views import *
from django.views.generic import TemplateView
from functools import wraps
from django.http import HttpResponseRedirect

urlpatterns=[
    
    url(r'^index$',index,name="index"),
    url(r'^login$',login,name="login"),
    url(r'^user_logout$',user_logout,name="user_logout"),

    url(r'^register$',register,name="register"),
    url(r'^updatePassword$',updatePassword,name="updatePassword"),
    # url(r'^Get_Model$',get_model,name="Get_Model"),

]
