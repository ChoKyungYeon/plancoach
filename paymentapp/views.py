from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from documentapp.models import Document
from paymentapp.decorators import *
try:#deploy check
    from plancoach.settings.local import PORTONE_SHOP_ID
except:
    from plancoach.settings.deploy import PORTONE_SHOP_ID

from paymentapp.forms import PaymentCreateForm
from paymentapp.models import Payment

@login_required
@PaymentCreateDecorater
def PaymentCreateView(request, pk):
    target_consult = get_object_or_404(Consult, pk=pk)
    if request.method == 'POST':
        form = PaymentCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                target_consult.payment.filter(is_paid_ok=False).delete()
                form.instance.classname = target_consult.consult_name()
                form.instance.amount = target_consult.tuition
                form.instance.consult = target_consult
                form.instance.save()
                return redirect('paymentapp:pay', pk=form.instance.pk)
    else:
        form = PaymentCreateForm()

    context = {
        'form': form,
        'target_consult': target_consult,
        'startdate' : datetime.now().date(),
        'enddate' : datetime.now().date()+timedelta(days=28),
        'extenddate': target_consult.extenddate() if target_consult.extenddate() else None
    }
    return render(request, 'paymentapp/create.html', context)


@login_required
@PaymentPayDecorater
def PaymentPayView(request, pk):
    target_user=request.user
    payment = get_object_or_404(Payment, pk=pk)
    payment_props = {
        "merchant_uid": payment.merchant_uid,
        'buyer_email': target_user.email,
        'buyer_name': target_user.userrealname,
        "name": payment.classname,
        "amount": payment.amount,
    }
    check_url = reverse('paymentapp:check', args=[payment.pk])

    portone_shop_id =PORTONE_SHOP_ID  #deploy 바꿔주기
    return render(request,
              'paymentapp/pay.html',
              {
                  'check_url': check_url,
                  'payment_props': payment_props,
                  'portone_shop_id': portone_shop_id,
              }
              )


@login_required
@PaymentPayDecorater
def PaymentCheckView(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.portone_check()

    return redirect('paymentapp:result', pk=payment.pk)


@login_required
@PaymentResultDecorater
def PaymentResultView(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    context = {
        'payment': payment,
        'extenddate': payment.consult.extenddate() if payment.consult.extenddate() else None,
    }
    return render(request, 'paymentapp/result.html', context)



@method_decorator(login_required, name='dispatch')
@method_decorator(PaymentContactDecorater, name='dispatch')
class PaymentContactView(TemplateView):
    template_name = 'paymentapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = Document.objects.all().first()
        context['target_payment'] = get_object_or_404(Payment, pk=self.kwargs['pk'])
        context['document']=Document.objects.all().first()
        return context