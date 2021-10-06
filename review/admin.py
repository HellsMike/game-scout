from django.contrib import admin
from .models import Review


# Admin models needed to change admin interface
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'rate', 'product', 'date')
    list_filter = ('product', 'date')
