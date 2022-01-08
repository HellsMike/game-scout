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
]
