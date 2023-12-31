from django import forms

from consultapp.models import Consult
from paymentapp.models import Payment
from plancoach.widgets import CustomSelect


class PaymentCreateForm(forms.ModelForm):
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





