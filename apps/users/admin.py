from django.contrib import admin
from apps.users.models import (
    CustomUser
)
# from django.contrib.auth.admin import UserAdmin


# Register your models here.


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('email', 'username')


admin.site.register(CustomUser, UserModelAdmin)
