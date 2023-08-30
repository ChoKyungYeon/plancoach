from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .forms import AccountCreateAdminForm, AccountUpdateAdminForm
from .models import CustomUser
from django.contrib.auth.models import Group


admin.site.unregister(Group)
admin.site.site_header = 'Plan&Coach 관리자 페이지'
admin.site.index_title = ""


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('display_customUser',)
    readonly_fields = ('display_user_info','display_consult_info')
    add_fields = ('username','email','userrealname','password1', 'password2')
    change_fields = ('display_user_info','display_consult_info','state','password1', 'password2')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fields = self.add_fields
            return AccountCreateAdminForm
        else:
            self.fields = self.change_fields
            return AccountUpdateAdminForm

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def display_customUser(self, obj):
        return f"[{obj.get_state_display()}] {obj.userrealname} {obj.username}"

    display_customUser.short_description = ''

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.opts.verbose_name = '사용자'
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "변경 사용자 선택"
        return super(CustomUserAdmin, self).changelist_view(request, extra_context=extra_context)

    def display_user_info(self, obj):
        return format_html(
            "<strong>PK:</strong> {}<br>"
            "<strong>상태:</strong> {}<br>"
            "<strong>실명:</strong> {}<br>"
            "<strong>이메일:</strong> {}<br>"
            "<strong>연락처:</strong> {}",
            obj.pk,
            obj.get_state_display(),
            obj.userrealname,
            obj.email,
            obj.username
        )
    display_user_info.short_description = '사용자 정보'

    def display_consult_info(self, obj):
        if obj.state == 'teacher':
            consults=obj.consult_teacher.all()
            consult_classname =", ".join("<{}>".format(consult.consult_name()) for consult in obj.consult_teacher.all()) \
                if consults else '진행 컨설팅이 없습니다'
            return format_html(
                "<strong>모집 정보:</strong> {}<br>"
                "<strong>컨설팅료:</strong> {}<br>"
                "<strong>진행 컨설팅 목록:</strong> {}",
                obj.profile.get_state_display(),
                obj.profile.tuition,
                consult_classname
            )
        elif obj.state == 'student':
            consult = getattr(self, 'consult_student', None)
            consult_classname = f'<{consult.consult_name()}>' if consult else '진행 컨설팅이 없습니다'
            application = getattr(self, 'application_student', None)
            application_name = f'<{application.teacher.userrealname} 신청서>' if application else '신청서가 없습니다'
            return format_html(
                "<strong>신청서:</strong> {}<br>"
                "<strong>진행 컨설팅:</strong> {}",
                application_name,
                consult_classname
            )
        else:
            return format_html(
                "<strong>진행 컨설팅:</strong> {}",
                '관리자 계정'
            )
    display_consult_info.short_description = '컨설팅 정보'

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['password1'] == form.cleaned_data['password2']:
            obj.set_password(form.cleaned_data['password1'])
        else:
            raise ValidationError("Passwords do not match")
        super().save_model(request, obj, form, change)
admin.site.register(CustomUser, CustomUserAdmin)