from django.contrib import admin
from .models import Refund
from .forms import RefundCreateFormAdmin
from django.contrib.admin import ModelAdmin

class RefundAdmin(ModelAdmin):
    form = RefundCreateFormAdmin
    list_display = ('classname','created_at','amount','salary')
admin.site.register(Refund, RefundAdmin)

