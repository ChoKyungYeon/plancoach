from django.contrib import admin
from .models import Refund

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'classname', 'created_at', 'amount', 'is_given', 'bank', 'accountnumber', 'depositor', 'given_at')  # Fields you want to see in the list view
    search_fields = ('classname', 'bank', 'accountnumber', 'depositor')  # Fields you want to search by
    list_filter = ('is_given', 'created_at', 'bank')  # Fields you want to filter by
