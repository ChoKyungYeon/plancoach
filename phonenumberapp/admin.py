from django.contrib import admin
from .models import Phonenumber
from django.contrib.admin import ModelAdmin

class PhonenumberAdmin(ModelAdmin):
    list_display = ('phonenumber',)
admin.site.register(Phonenumber, PhonenumberAdmin)