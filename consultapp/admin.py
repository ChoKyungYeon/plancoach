from django.contrib import admin
from .models import Consult
from .forms import  ConsultAdminForm
from django.contrib.admin import ModelAdmin

class ConsultAdmin(ModelAdmin):
    form = ConsultAdminForm
    list_display = ('pk','student','teacher','state','tuition','startdate')
admin.site.register(Consult, ConsultAdmin)

