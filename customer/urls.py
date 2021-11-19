from django.urls import path
from . import  views

app_name = 'customer'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('user', views.user, name='user'),
]
