from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'is_seller', 'get_sold_keys', 'get_ratings')
    list_filter = ('is_staff', 'groups')

    def is_seller(self, obj):
        return obj.groups.filter(name='Sellers').exists()

    def get_sold_keys(self, obj):
        return Profile.objects.get(user=obj).sold_keys

    def get_ratings(self, obj):
        return (Profile.objects.get(user=obj).seller_total_ratings)/(Profile.objects.get(user=obj).seller_ratings_count)