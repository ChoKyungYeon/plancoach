from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, RedirectView, DetailView
from consultapp.models import Consult
from plancoach.sms import Send_SMS
from plancoach.utils import salaryday_calculator
from refundapp.decorators import *
from refundapp.forms import RefundCreateForm
from refundapp.models import Refund
from django.utils.decorators import method_decorator

from refusalapp.models import Refusal

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(RefundGuideDecorator, name='dispatch')
class RefundGuideView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'refundapp/guide.html'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(RefundCreateDecorator, name='dispatch')
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
        teacher = target_consult.teacher
        salaryday = salaryday_calculator(target_consult.enddate())
        target_salary = target_consult.teacher.salary.get(salaryday=salaryday)
        with transaction.atomic():
            # form instacne
            form.instance.classname = target_consult.consult_name()
            form.instance.student = target_consult.student
            form.instance.amount = target_consult.refund_amount()
            form.instance.salary = target_salary
            form.instance.save()
            # add object
            if target_consult.state == 'extended':
                extend_salaryday =salaryday_calculator(target_consult.extend_enddate())
                next_salary = target_consult.teacher.salary.get(salaryday=extend_salaryday)
                Refund.objects.create(
                    classname=form.instance.classname,
                    salary=next_salary,
                    student=form.instance.student,
                    amount=target_consult.tuition,
                    bank=form.instance.bank,
                    accountnumber=form.instance.accountnumber,
                    depositor=form.instance.depositor
                )
            target_consult.delete()
            # sendsms
            content = f'{form.instance.student.userrealname} 학생의 요청으로 컨설팅이 환불 처리되었습니다.'
            Send_SMS(teacher.username, content, teacher.can_receive_notification)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('studentapp:dashboard', kwargs={'pk': self.request.user.pk})


@method_decorator(login_required, name='dispatch')
@method_decorator(RefundStateUpdateDecorator, name='dispatch')
class RefundStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('superuserapp:dashboard')

    def get(self, request, *args, **kwargs):
        refund = Refund.objects.get(pk=self.request.GET.get('refund_pk'))
        student = refund.student
        with transaction.atomic():
            refund.is_given= True
            refund.given_at= datetime.now()
            refund.save()
            content = f'요청하신 환불이 정상 처리되었습니다.'
            Send_SMS(student.username, content, student.can_receive_notification)
            Refusal.objects.filter(student=student).delete()
            Refusal.objects.create(student=student, type='refund')
            return super(RefundStateUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(RefundDetailDecorator, name='dispatch')
class RefundDetailView(DetailView):
    model = Refund
    context_object_name = 'target_refund'
    template_name = 'refundapp/detail.html'

@method_decorator(login_required, name='dispatch')
@method_decorator(RefundPayDecorator, name='dispatch')
class RefundPayView(DetailView):
    model = Refund
    context_object_name = 'target_refund'
    template_name = 'refundapp/pay.html'

