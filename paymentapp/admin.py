from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'classname', 'created_at', 'amount', 'is_paid_ok')
    search_fields = ('classname', 'amount')
    list_filter = ('is_paid_ok', 'created_at')

    fields = ('classname', 'created_at', 'amount', 'is_paid_ok', 'salary')  # All fields you want to display
    readonly_fields = ('classname', 'created_at', 'amount', 'is_paid_ok')  # Fields you don't want to edit