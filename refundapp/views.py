from datetime import date, datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, RedirectView, TemplateView, DetailView

from accountapp.models import CustomUser
from consultapp.models import Consult
from plancoach.sms import Send_SMS
from plancoach.updaters import request_user_updater
from paymentapp.models import Payment
from refundapp.forms import RefundCreateForm
from refundapp.models import Refund
from salaryapp.utils import salaryday_calculator


class RefundGuideView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'refundapp/guide.html'

# Create your views here.
@method_decorator(request_user_updater, 'get')
class RefundCreateView(CreateView):
    model = Refund
    form_class = RefundCreateForm
    template_name = 'refundapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult=get_object_or_404(Consult, pk=self.kwargs['pk'])
        context['target_consult'] = target_consult
        return context

    def form_valid(self, form):
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        teacher=target_consult.teacher
        with transaction.atomic():
            form.instance.classname = target_consult.consult_name()
            form.instance.student = target_consult.student
            salaryday = salaryday_calculator(target_consult.enddate())
            form.instance.amount = target_consult.refund_amount()
            target_salary = target_consult.teacher.salary.get(salaryday=salaryday)
            form.instance.salary = target_salary
            form.instance.save()
            if target_consult.state == 'extended':
                extend_salaryday =salaryday_calculator(target_consult.extend_enddate())
                next_salary = target_consult.teacher.salary.get(salaryday=extend_salaryday)
                Refund.objects.create(
                    classname=form.instance.classname,
                    salary=next_salary,
                    student=form.instance.student,
                    amount=target_consult.tuition*10000,
                    bank=form.instance.bank,
                    accountnumber=form.instance.accountnumber,
                    depositor=form.instance.depositor
                )

            target_consult.delete()
            target_consult.application.delete()
            return super().form_valid(form)
            content = f'({self.classname}) 수업이 환불 처리 되었습니다.'
            Send_SMS(teacher.username, content, teacher.can_receive_notification)
            print('done')

    def get_success_url(self):
        return reverse('studentapp:dashboard', kwargs={'pk': self.request.user.pk})

#1 로그인 2 소유자(선생만) 4step3
@method_decorator(request_user_updater, 'get')
class RefundStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        refund = Refund.objects.get(pk=self.request.GET.get('refund_pk'))
        with transaction.atomic():
            student=refund.student
            content = f'({refund.classname}) 수업이 환불 완료되었습니다.'
            Send_SMS(student.username, content, student.can_receive_notification)
        return reverse_lazy('superuserapp:dashboard')
    def get(self, request, *args, **kwargs):
        refund = Refund.objects.get(pk=self.request.GET.get('refund_pk'))
        refund.is_given = True
        refund.save()
        return super(RefundStateUpdateView, self).get(request, *args, **kwargs)



class RefundDetailView(DetailView):
    model = Refund
    context_object_name = 'target_refund'
    template_name = 'refundapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

