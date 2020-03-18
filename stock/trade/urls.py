from django.urls import path
from django.conf.urls import url
from trade import views

urlpatterns = [
    url('index', views.index, name='index'), 
    url('getStocksData',views.getStocksData,name='getStocksData'),
    url('getSymbolData',views.getSymbolData,name='getSymbolData'),
]