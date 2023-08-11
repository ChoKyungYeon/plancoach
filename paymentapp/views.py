from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, CreateView, DetailView, RedirectView, DeleteView
from django.utils.decorators import method_decorator

from depositapp.models import Deposit
from documentapp.models import Document
from paymentapp.decorators import *
from plancoach.sms import Send_SMS



from paymentapp.forms import PaymentCreateForm
from paymentapp.models import Payment

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentCreateDecorator, name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    template_name = 'paymentapp/create.html'
    form_class = PaymentCreateForm

    def form_valid(self, form):
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        classname = target_consult.consult_name()
        with transaction.atomic():
            form.instance.classname = classname
            form.instance.amount = target_consult.tuition
            form.instance.consult = target_consult
            form.instance.student = target_consult.student
            form.instance.save()

            content = f'{classname} 입금을 확인하세요'
            phonenumber = Document.objects.all().first().phonenumber
            if phonenumber:
                Send_SMS(phonenumber, content, True)
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['target_consult'] = target_consult
        context['depositbank'] = Deposit.objects.all().first()
        context['startdate'] = datetime.now().date()
        context['enddate'] = datetime.now().date()+timedelta(days=28)
        context['extenddate'] = target_consult.extenddate() if target_consult.extenddate() else None
        return context

    def get_success_url(self):
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        return reverse_lazy('studentapp:dashboard', kwargs={'pk': target_consult.student.pk}) if target_consult.state == 'new' else \
            reverse_lazy('consultapp:waiting', kwargs={'pk': target_consult.pk})


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentGuideDecorator, name='dispatch')
class PaymentGuideView(TemplateView):
    template_name = 'paymentapp/guide.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_consult'] = get_object_or_404(Consult, pk=self.kwargs['pk'])
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentPayDecorator, name='dispatch')
class PaymentPayView(DetailView):
    model = Payment
    context_object_name = 'target_payment'
    template_name = 'paymentapp/pay.html'

    def get_context_data(self, **kwargs):
        target_consult = get_object_or_404(Payment, pk=self.kwargs['pk']).consult
        context = super().get_context_data(**kwargs)
        context['target_consult'] = target_consult
        context['startdate'] = datetime.now().date()
        context['enddate'] = datetime.now().date()+timedelta(days=28)
        context['extenddate'] = target_consult.extenddate() if target_consult.extenddate() else None
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentStateUpdateDecorator, name='dispatch')
class PaymentStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('superuserapp:dashboard')

    def get(self, request, *args, **kwargs):
        payment = Payment.objects.get(pk=self.request.GET.get('payment_pk'))
        with transaction.atomic():
            payment.update()
            content = '입금 요청이 확인 완료되었습니다. 컨설팅을 시작해 주세요!'
            Send_SMS(payment.student.username, content, payment.student.can_receive_notification)
            return super(PaymentStateUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentDeleteDecorator, name='dispatch')
class PaymentDeleteView(DeleteView):
    model = Payment
    context_object_name = 'target_payment'
    template_name = 'paymentapp/delete.html'

    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')
