from django import forms
from django.forms import ModelForm

from depositapp.models import Deposit
from plancoach.widgets import CustomSelect


class DepositCreateForm(ModelForm):
    class Meta:
        model = Deposit
        fields = ('bank','accountnumber','depositor')
        labels = {
            'bank':'은행',
            'accountnumber':'계좌 번호',
            'depositor':'예금주명',
        }

        widgets = {
            'bank': CustomSelect(attrs={'placeholder': '', 'class': 'select'}),
            'accountnumber': forms.NumberInput(attrs={'placeholder': '- 제외 숫자만 입력','class': 'textinput',}),
            'depositor': forms.TextInput(attrs={'placeholder': '본인 명의의 계좌를 입력해 주세요', 'class': 'textinput' }),
        }

