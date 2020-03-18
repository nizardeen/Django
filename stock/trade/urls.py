from django.urls import path
from trade import views

urlpatterns = [
    url('index', views.index, name='index'), 
]