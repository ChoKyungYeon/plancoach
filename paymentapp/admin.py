from datetime import datetime, timedelta

from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from plancoach.sms import Send_SMS
from plancoach.utils import salaryday_calculator
from salaryapp.models import Salary
from .forms import PaymentCreateAdminForm, PaymentUpdateAdminForm
from django.contrib.auth.models import Group

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('display_payment',)
    readonly_fields = ('display_payment_info',)
    add_fields = ('consult',)
    change_fields = ('display_payment_info',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_paid_ok=True)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fields = self.add_fields
            return PaymentCreateAdminForm
        else:
            self.fields = self.change_fields
            return PaymentUpdateAdminForm

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def display_payment(self, obj):
        return f"[{obj.classname}] {obj.amount}원 {obj.created_at.strftime('%Y-%m-%d %H:%M')} "

    display_payment.short_description = ''

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.opts.verbose_name = '입금 내역'
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "변경 입금내역 선택"
        return super(PaymentAdmin, self).changelist_view(request, extra_context=extra_context)

    def display_payment_info(self, obj):
        return format_html(
            "<strong>수업명:</strong> {}<br>"
            "<strong>입금액:</strong> {}<br>"
            "<strong>첫 입금:</strong> {}<br>"
            "<strong>입금일:</strong> {}<br>"
            "<strong>급여 날짜:</strong> {} <strong>급자:</strong> {}<br>",
            obj.classname,
            obj.amount,
            obj.is_initial_payment,
            obj.created_at,
            obj.salary.salaryday,
            obj.salary.teacher,
        )
    display_payment_info.short_description = '입금 정보'

    def save_model(self, request, obj, form, change):
        def new_payment_process(obj, consult, teacher):
            consult.state = 'unextended'
            consult.startdate = obj.created_at.date()
            consult.save()

            salaryday = salaryday_calculator(obj.created_at.date() + timedelta(days=28))
            add_salary(obj, teacher, salaryday)
            content = f'{consult.student.userrealname} 학생의 신규 입금이 완료되었습니다. 컨설팅을 시작해 주세요!'
            Send_SMS(teacher.username, content, teacher.can_receive_notification)

        def extend_payment_process(obj, consult, teacher):
            consult.state = 'extended'
            consult.save()

            salaryday = salaryday_calculator(obj.created_at.date() + timedelta(days=57))
            add_salary(obj, teacher, salaryday)

            content = f'{consult.student.userrealname} 학생의 컨설팅 연장이 완료되었습니다!'
            Send_SMS(teacher.username, content, teacher.can_receive_notification)

        def add_salary(obj,teacher, salaryday):
            try:
                obj.salary = teacher.salary.get(salaryday=salaryday)
            except:
                Salary.objects.create(teacher=teacher, salaryday=salaryday)
                obj.salary = teacher.salary.get(salaryday=salaryday)

        with transaction.atomic():
            # check if it's a new object and not an update
            if not change:
                consult = obj.consult
                obj.classname = consult.consult_name()
                obj.status = '결제완료'
                obj.amount = consult.tuition
                obj.created_at = datetime.now()
                obj.is_paid_ok = True
                obj.is_checked = True
                teacher = consult.teacher
                if consult.state == 'new':
                    new_payment_process(obj,consult, teacher)
                else:
                    extend_payment_process(obj,consult, teacher)

            obj.save()

admin.site.register(Payment, PaymentAdmin)