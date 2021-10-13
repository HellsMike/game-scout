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
    list_display = ('username', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('is_staff',)

    # def seller(self, obj):
    #     sell_filter = Profile.objects.filter(user=obj)
    #     return sell_filter['is_seller']
