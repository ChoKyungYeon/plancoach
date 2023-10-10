from django.contrib import admin

from paymentapp.models import Payment
from refundapp.models import Refund
from .models import Salary

class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0
    readonly_fields = ('display_refund',)

    def display_refund(self, obj):
        return str(obj)
    display_refund.short_description = 'Refund'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('display_payment',)

    def display_payment(self, obj):
        return str(obj)
    display_payment.short_description = 'Payment'  # Changed from 'Refund' to 'Payment'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('salaryday', 'teacher', 'is_given', 'given_at')
    search_fields = ('salaryday', 'teacher')

    fields = ('salaryday', 'teacher', 'is_given', 'given_at')
    readonly_fields = ('salaryday', 'teacher', 'is_given', 'given_at')
    ordering = ('-salaryday',)
    inlines = [RefundInline, PaymentInline]