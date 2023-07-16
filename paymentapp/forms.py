
from django import forms
from django.forms import  ModelForm

from paymentapp.models import Payment


class PaymentForm(ModelForm):

    class Meta:
        model = Payment
        fields = ('classname', 'amount')
        labels = {
            # your labels here
        }
        widgets = {
            'classname': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classname'].required = False
        self.fields['amount'].required = False

class PaymentCreateFormAdmin(ModelForm):

    class Meta:
        model = Payment
        fields = ('classname', 'amount','consult','is_paid_ok')