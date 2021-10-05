from django.contrib import admin
from .models import Category, Genre, Developer, Publisher, Transaction, Product, Key


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Developer)
admin.site.register(Publisher)
admin.site.register(Transaction)
admin.site.register(Product)
admin.site.register(Key)
