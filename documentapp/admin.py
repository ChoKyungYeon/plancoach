from django.contrib import admin
from .models import Document
from .forms import  DocumentAdminForm
from django.contrib.admin import ModelAdmin

class DocumentAdmin(ModelAdmin):
    form = DocumentAdminForm
    list_display = ('pk','refund','termofuse','privacypolicy','kakaotalk')
admin.site.register(Document, DocumentAdmin)

