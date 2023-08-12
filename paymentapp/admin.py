from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'classname', 'created_at', 'amount', 'is_paid_ok')  # Fields you want to see in the list view
    search_fields = ('classname', 'amount')  # Fields you want to search by
    list_filter = ('is_paid_ok', 'created_at')