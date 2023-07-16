from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm

from phonenumberapp.models import Phonenumber


class PhonenumberCreateForm(ModelForm):
    class Meta:
        model = Phonenumber
        fields = ('phonenumber',)
        labels = {
            'phonenumber': '전화번호'
        }

        widgets = {
            'phonenumber': forms.NumberInput(attrs={'placeholder': '- 제외 전화번호 11자',
                                                    'class': 'textinput','oninput': 'this.value = this.value.slice(0, 11);'}),

        }

class PhoneNumberVerifyForm(forms.Form):
    compare_code = forms.CharField(
        label="인증 코드",
        widget=forms.NumberInput(attrs={'placeholder': '인증 코드를 입력하세요', 'class': 'textinput',
                                        'oninput': 'this.value = this.value.slice(0, 6);'}),
    )
