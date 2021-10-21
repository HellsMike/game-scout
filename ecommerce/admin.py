from django.contrib import admin
from .models import *


# Admin models needed to change admin interface
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'key')
    list_filter = ('date',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'publisher', 'publishing_date')
    list_filter = ('category', 'genre', 'developer', 'publisher', 'publishing_date')


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('serial_key', 'product', 'price')
    list_filter = ('product', 'price', 'sold')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass


@admin.register(SellerLibrary)
class SellerLibraryAdmin(admin.ModelAdmin):
    pass

