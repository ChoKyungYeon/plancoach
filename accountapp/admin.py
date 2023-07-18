from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import AccountCreateFormAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    form = AccountCreateFormAdmin
    model = CustomUser
    list_display = ['username', 'email', 'userrealname', 'state']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('userrealname', 'email', 'state')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
