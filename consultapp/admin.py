from django.contrib import admin

from consult_qnaapp.models import Consult_qna
from consultapp.models import Consult
from qna_commentapp.models import Qna_comment


class Qna_commentInline(admin.TabularInline):
    model = Qna_comment
    extra = 0
    readonly_fields = ['image', 'content', 'created_at']
    can_delete = False
    max_num = 0

class Consult_qnaInline(admin.TabularInline):
    model = Consult_qna
    extra = 0
    readonly_fields = ['image', 'title', 'content', 'created_at']
    inlines = [Qna_commentInline]
    can_delete = False
    max_num = 0

class ConsultAdmin(admin.ModelAdmin):
    list_display = ['student', 'teacher', 'state', 'tuition', 'created_at']
    inlines = [Consult_qnaInline]
    can_delete = False

admin.site.register(Consult, ConsultAdmin)
