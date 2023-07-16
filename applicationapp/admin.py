from django.contrib import admin
from .models import Application
from .forms import ApplicationAdminForm
from django.contrib.admin import ModelAdmin

class ApplicationAdmin(ModelAdmin):
    form = ApplicationAdminForm
    list_display = ('pk','student','teacher')
admin.site.register(Application, ApplicationAdmin)

