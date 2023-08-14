from django.contrib import admin
from apps.users.models import (
    CustomUser
)

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('email', 'username')


admin.site.register(CustomUser, UserAdmin)
