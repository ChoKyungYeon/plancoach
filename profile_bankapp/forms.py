from django import forms
from django.forms import ModelForm

from profile_bankapp.models import Profile_bank
from plancoach.widgets import CustomSelect


class Profile_bankUpdateForm(ModelForm):
    class Meta:
        model = Profile_bank
        fields = ('bank','accountnumber','depositor')
        labels = {
            'bank':'* 은행',
            'accountnumber':'* 계좌 번호',
            'depositor':'* 예금자명',
        }

        widgets = {
            'bank': CustomSelect(attrs={'placeholder': '', 'class': 'select'}),
            'accountnumber': forms.NumberInput(attrs={'placeholder': '- 제외 숫자만 입력','class': 'textinput',}),
            'depositor': forms.TextInput(attrs={'placeholder': '실명과 일치', 'class': 'textinput' }),
        }

