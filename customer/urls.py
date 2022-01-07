from django.urls import path
from . import  views

app_name = 'customer'

urlpatterns = [
    path('keymanager', views.keymanager, name=''),
    path('library', views.library, name=''),
    path('settings', views.profilesettings, name=''),
    path('signup', views.signup, name='signup'),
    path('wishlist', views.wishlist, name=''),
    path('become-seller', views.becomeseller, name='become-seller'),
    path('become-customer', views.becomecustomer, name='become-customer'),
    # path('user', views.user, name='user'),
    # path('provaform', views.provaform, name=''),
]
