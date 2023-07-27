from django import forms
from django.forms import ModelForm
from plancoach.widgets import CustomSelect
from applicationapp.models import Application


class ApplicationCreateForm(ModelForm):
    class Meta:
        model = Application
        fields = ('belong', 'age', 'strategy', 'problem', 'want')
        labels = {
            'belong': '소속 및 상황',
            'age': '학년',
            'strategy': '희망 전형',
            'problem': '현재 성적 및 상황',
            'want': '바라는 컨설팅 방식'
        }

        widgets = {
            'belong': forms.TextInput(attrs={'placeholder': '00 재수학원, 00 고등학교, 군인, 대학생 등', 'class': 'textinput'}),
            'age': CustomSelect(attrs={'class': 'select', }),
            'strategy': forms.TextInput(attrs={'placeholder': '정시, 수시 및 상세 입시 전형', 'class': 'textinput'}),
            'problem': forms.Textarea(attrs={'placeholder': '1 모의고사 및 내신 성적, 2 선생님이 알아야 할 점 등', 'class': 'textarea'}),
            'want': forms.Textarea(attrs={'placeholder': '1 수업 가능 요일/시간, 2 개선하고 싶은 점, 3 원하는 수업 스타일 등', 'class': 'textarea'}),
        }

