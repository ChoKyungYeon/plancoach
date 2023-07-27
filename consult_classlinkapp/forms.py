from django import forms
from django.forms import ModelForm
from consult_classlinkapp.models import Consult_classlink
from plancoach.widgets import CustomSelect


class Consult_classlinkCreateForm(ModelForm):
    class Meta:
        model = Consult_classlink
        fields = ('weekdate', 'classtime', 'link')
        labels = {
            'weekdate': '수업 요일',
            'classtime': '수업 시간',
            'link': '수업 링크 ',
        }

        widgets = {
            'weekdate': CustomSelect(attrs={'class': 'select', }),
            'classtime': forms.TextInput(attrs={'placeholder': '오전/오후 00시', 'class': 'textinput', }),
            'link': forms.Textarea(attrs={'placeholder': '구글 Meet 초대 링크를 입력해주세요', 'class': 'textarea', }),
        }
