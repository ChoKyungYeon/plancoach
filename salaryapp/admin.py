from django.contrib import admin
from .models import Salary
from .forms import SalaryCreateFormAdmin
from django.contrib.admin import ModelAdmin

class SalaryAdmin(ModelAdmin):
    form = SalaryCreateFormAdmin
    list_display = ('salaryday', 'teacher','bank','accountnumber','depositor','is_given','given_at')
admin.site.register(Salary, SalaryAdmin)

