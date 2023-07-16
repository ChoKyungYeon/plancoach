from django.contrib import admin
from .models import Payment
from .forms import PaymentCreateFormAdmin
from django.contrib.admin import ModelAdmin

class PaymentAdmin(ModelAdmin):
    form = PaymentCreateFormAdmin
    list_display = ('classname','created_at','is_paid_ok','amount','salary')
admin.site.register(Payment, PaymentAdmin)

