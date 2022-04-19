from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('catalog', views.catalog, name='catalog'),
    path('scout', views.scout, name='scout'),
    path('search', views.search, name='search'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart', views.remove_from_cart, name='remove-from-cart'),
    path('buy-keys', views.buy_keys, name='buy-keys'),
    path('product-add', views.product_add, name='product-add'),
]
