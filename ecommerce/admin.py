from django.contrib import admin
from .models import Transaction, Product, Key


admin.site.register(Transaction)
admin.site.register(Product)
admin.site.register(Key)
