from audioop import reverse

from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DetailView, RedirectView

from plancoach.sms import Send_SMS
from salaryapp.models import Salary
from plancoach.updaters import *
from django.utils.decorators import method_decorator


class SalaryDetailView(DetailView):
    model = Salary
    context_object_name = 'target_salary'
    template_name = 'salaryapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payment.all()
        context['refunds'] = self.object.refund.all()
        context['target_bank'] = self.object.teacher.profile.profile_bank
        return context

class SalaryExpectedView(DetailView):
    model = Salary
    context_object_name = 'target_salary'
    template_name = 'salaryapp/expected.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payment.all()
        context['refunds'] = self.object.refund.all()
        return context

class SalaryPayView(DetailView):
    model = Salary
    context_object_name = 'target_salary'
    template_name = 'salaryapp/pay.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payment.all()
        context['refunds'] = self.object.refund.all()
        context['target_bank'] = self.object.teacher.profile.profile_bank
        return context

class SalaryStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('superuserapp:dashboard')

    def get(self, request, *args, **kwargs):
        salary = Salary.objects.get(pk=self.request.GET.get('salary_pk'))
        teacher = salary.teacher
        bank = teacher.profile.profile_bank
        with transaction.atomic():
            # form instacne
            salary.is_given = True
            salary.bank=bank.bank
            salary.accountnumber=bank.accountnumber
            salary.depositor=bank.depositor
            salary.given_at = datetime.now()
            salary.save()
            # sendsms
            content = f'{salary.salaryday}급여 {salary.paid_amount()}원 입금이 완료되었습니다'
            Send_SMS(teacher.username, content, teacher.can_receive_notification)
            return super(SalaryStateUpdateView, self).get(request, *args, **kwargs)
