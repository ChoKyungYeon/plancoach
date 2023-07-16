from django.contrib import admin
from .models import Profile
from .forms import ProfileCreateForm
from django.contrib.admin import ModelAdmin

class ProfileAdmin(ModelAdmin):
    form = ProfileCreateForm
    list_display = ['pk','teacher']
admin.site.register(Profile, ProfileAdmin)


