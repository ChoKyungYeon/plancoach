from django.contrib import admin
from .models import Document
from .forms import DocumentAdminForm
from django.contrib.admin import ModelAdmin


class DocumentAdmin(ModelAdmin):
    form = DocumentAdminForm
    list_display = ('pk', 'refund', 'termofuse', 'privacypolicy', 'kakaotalk',
                    'termofuse_updated','refund_updated','privacypolicy_updated')


admin.site.register(Document, DocumentAdmin)
