from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from refundapp.models import Refund


class RefundCreateForm(ModelForm):
    class Meta:
        model = Refund
        fields = ('classname', 'amount','bank','accountnumber','depositor')
        labels = {
            'bank': '은행',
            'accountnumber': '계좌 번호',
            'depositor': '예금자명 (실명과 일치해야 합니다)',
        }
        widgets = {
            'classname': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
            'bank': CustomSelect(attrs={'placeholder': '', 'class': 'select'}),
            'accountnumber': forms.NumberInput(attrs={'placeholder': '- 제외 숫자만 입력', 'class': 'textinput', }),
            'depositor': forms.TextInput(attrs={'placeholder': '실명과 일치','class': 'select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classname'].required = False
        self.fields['amount'].required = False

class RefundCreateFormAdmin(ModelForm):
    class Meta:
        model = Refund
        fields = ('classname', 'amount','salary','is_given')