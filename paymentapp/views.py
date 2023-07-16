from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView
from consultapp.models import Consult
from plancoach.variables import current_date

try:#deploy check
    from plancoach.settings.local import PORTONE_SHOP_ID
except:
    from plancoach.settings.deploy import PORTONE_SHOP_ID

from plancoach.updaters import request_user_updater
from paymentapp.forms import PaymentForm
from paymentapp.models import Payment


# Create your views here.
@request_user_updater
def PaymentCreateView(request, pk):
    target_consult = get_object_or_404(Consult, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            target_consult.payment.filter(is_paid_ok =False).delete()
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.classname = target_consult.consult_name()
                payment.amount = target_consult.tuition * 10 #deploy check
                payment.consult = target_consult
                payment.save()
                return redirect('paymentapp:pay', pk=payment.pk)
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'target_consult': target_consult,
        'startdate' : current_date,
        'extenddate': target_consult.extenddate() if target_consult.extenddate() else None
    }

    return render(request, 'paymentapp/create.html', context)

@request_user_updater
def PaymentPayView(request, pk):
    user=request.user
    payment = get_object_or_404(Payment, pk=pk)
    payment_props = {
        "merchant_uid": payment.merchant_uid,
        'buyer_email': user.email,
        'buyer_name': user.userrealname,
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


@request_user_updater
def PaymentCheckView(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.portone_check()

    return redirect('paymentapp:result', pk=payment.pk)


@request_user_updater
def PaymentResultView(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    context = {
        'payment': payment,
        'extenddate': payment.consult.extenddate() if payment.consult.extenddate() else None,

    }
    return render(request, 'paymentapp/result.html', context)



@method_decorator(request_user_updater, 'get')
class PaymentContactView(TemplateView):
    template_name = 'paymentapp/contact.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_payment = get_object_or_404(Payment, pk=self.kwargs['pk'])
        context['target_consult'] = target_payment.consult
        return context