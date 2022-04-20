from django.urls import path
from . import  views

app_name = 'review'

urlpatterns = [
    path('review/<int:prod_id>', views.review, name='review'),
]
