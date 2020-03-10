from django.conf.urls import url,include
from django.contrib import admin
from demo import views

urlpatterns=[
	url(r'^index$',views.index,name="index"),
    url(r'^delete/(?P<mobile>[0-9/]+)/(?P<id>\S+)$',views.delete,name="delete"),
]