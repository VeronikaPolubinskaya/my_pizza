# from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'pizza'

urlpatterns = [
    path('', views.pizza_list, name='pizza_list'),
    path('sauce/', views.sauce_list, name='sauce_list'),
]