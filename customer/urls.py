from django.urls import path
from . import  views

app_name = 'customer'

urlpatterns = [
    path('keymanager', views.keymanager, name=''),
    path('library', views.library, name=''),
    path('settings', views.profilesettings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('wishlist', views.wishlist, name=''),
    path('become-seller', views.becomeseller, name='become-seller'),
    path('become-customer', views.becomecustomer, name='become-customer'),
    path('add-key-confirmation', views.addkeyconfirmation, name='add-key-confirmation'),

    path('add-to-wishlist', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-to-wishlist', views.remove_to_wishlist, name='remove-to-wishlist'),
    # path('user', views.user, name='user'),
    # path('provaform', views.provaform, name=''),

    # path('provaform', views.change_pro_pic, name='provaform'),
    path('add-key', views.add_key, name='add-key'),
    path('delete-key', views.delete_key_by_seller, name='delete-key'),
]
