from django.urls import path
from . import  views

app_name = 'customer'

urlpatterns = [
    path('keymanager', views.keymanager, name=''),
    path('library', views.library, name=''),
    path('settings', views.profilesettings, name=''),
    path('signup', views.signup, name='signup'),
    path('wishlist', views.wishlist, name='signup'),
    path('user', views.user, name='user'),
]
