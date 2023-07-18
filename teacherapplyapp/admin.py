from django.contrib import admin
from .models import Teacherapply
from django.contrib.admin import ModelAdmin

class TeacherapplyAdmin(ModelAdmin):
    list_display = ('customuser',)
admin.site.register(Teacherapply, TeacherapplyAdmin)

