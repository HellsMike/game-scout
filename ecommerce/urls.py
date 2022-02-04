from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product', views.product, name='product'),
    path('cart', views.cart, name=''),
    path('catalog', views.catalog, name=''),
    path('scout', views.scout, name=''),
    path('search', views.search, name=''),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart', views.remove_from_cart, name='remove-from-cart'),
    path('buy-keys', views.buy_keys, name='buy-keys'),
]
