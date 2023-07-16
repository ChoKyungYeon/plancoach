from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from refundapp.models import Refund
from teacherapplyapp.models import Teacherapply


class TeacherapplyInfoCreateForm(ModelForm):
    class Meta:
        model = Teacherapply
        fields = ('consulttype','school', 'major', 'studentid', 'accepttype')
        labels = {
            'consulttype': '가능 담당 수업',
            'school': '학교',
            'major': '전공',
            'studentid': '학번',
            'accepttype': '합격 전형',
        }
        widgets = {
            'school': CustomSelect(attrs={ 'class': 'select',}),
            'major': forms.TextInput(attrs={'placeholder': 'oo과', 'class': 'textinput'}),
            'studentid': CustomSelect(attrs={'class': 'select'}),
            'accepttype': CustomSelect(attrs={ 'class': 'select'}),
            'consulttype': forms.CheckboxSelectMultiple(attrs={ 'class': 'selectmultiple'}),
        }
class TeacherapplySchoolimageCreateForm(ModelForm):
    class Meta:
        model = Teacherapply
        fields = ('schoolimage',)
        labels = {
            'schoolimage':'',
        }

        widgets = {
            'schoolimage': forms.FileInput(attrs={'placeholder': '재학증명', 'class': 'fileinput'}),
        }
class TeacherapplyUserimageCreateForm(ModelForm):
    class Meta:
        model = Teacherapply
        fields = ('userimage',)
        labels = {
            'userimage':'',
        }

        widgets = {
            'userimage': forms.FileInput(attrs={'placeholder': '신원 증명', 'class': 'fileinput'}),
        }

class TeacherapplyBankCreateForm(ModelForm):
    class Meta:
        model = Teacherapply
        fields = ('bank','accountnumber','depositor')
        labels = {
            'bank':'은행',
            'accountnumber':'계좌 번호',
            'depositor':'예금자명 (실명과 일치해야 합니다)',
        }

        widgets = {
            'bank': CustomSelect(attrs={'placeholder': '', 'class': 'select',}),
            'accountnumber': forms.NumberInput(attrs={'placeholder': '- 제외 숫자만 입력','class': 'textinput',}),
            'depositor': forms.TextInput(attrs={'placeholder': '실명과 일치', 'class': 'textinput', }),
        }
