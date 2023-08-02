from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, CreateView, DetailView
from django.utils.decorators import method_decorator

from documentapp.models import Document
from paymentapp.decorators import *
try:#deploy check
    from plancoach.settings.local import PORTONE_SHOP_ID
except:
    from plancoach.settings.deploy import PORTONE_SHOP_ID

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
        with transaction.atomic():
            target_consult.payment.filter(is_paid_ok=False).delete()
            form.instance.classname = target_consult.consult_name()
            form.instance.amount = target_consult.tuition
            form.instance.consult = target_consult
            form.instance.save()
            return redirect('paymentapp:pay', pk=form.instance.pk)

    def get_context_data(self, **kwargs):
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['target_consult'] = target_consult
        context['startdate'] = datetime.now().date()
        context['enddate'] = datetime.now().date()+timedelta(days=28)
        context['extenddate'] = target_consult.extenddate() if target_consult.extenddate() else None
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentPayDecorator, name='dispatch')
class PaymentPayView(DetailView):
    model = Payment
    template_name = 'paymentapp/pay.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.request.user
        payment = self.get_object()
        context['payment_props'] = {
            "merchant_uid": payment.merchant_uid,
            'buyer_email': target_user.email,
            'buyer_name': target_user.userrealname,
            "name": payment.classname,
            "amount": payment.amount,
        }
        context['check_url'] = reverse('paymentapp:check', args=[payment.pk])
        context['portone_shop_id'] = PORTONE_SHOP_ID  # deploy 바꿔주기
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentPayDecorator, name='dispatch')
class PaymentCheckView(View):
    def get(self, request, *args, **kwargs):
        payment=get_object_or_404(Payment, pk=kwargs['pk'])
        payment.portone_check()
        return redirect(reverse('paymentapp:result', kwargs={'pk': payment.pk}))


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentResultDecorator, name='dispatch')
class PaymentResultView(TemplateView):
    template_name = 'paymentapp/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = get_object_or_404(Payment, pk=kwargs['pk'])
        context['payment'] = payment
        context['extenddate']=payment.consult.extenddate() if payment.consult.extenddate() else None,
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentContactDecorator, name='dispatch')
class PaymentContactView(TemplateView):
    template_name = 'paymentapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_payment'] = get_object_or_404(Payment, pk=self.kwargs['pk'])
        context['document']=Document.objects.all().first()
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentGuideDecorator, name='dispatch')
class PaymentGuideView(TemplateView):
    template_name = 'paymentapp/guide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_consult'] = get_object_or_404(Consult, pk=self.kwargs['pk'])
        return context
