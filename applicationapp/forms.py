from django import forms
from django.forms import ModelForm


from plancoach.widgets import CustomSelect
from applicationapp.models import Application


class ApplicationCreateForm(ModelForm):
    class Meta:
        model = Application
        fields = ('belong','age','strategy','problem','want')
        labels = {
            'belong':'소속',
            'age':'학년',
            'strategy':'입시 전략',
            'problem':'현재 성적과 문제점',
            'want':'원하는 수업 방식'
        }

        widgets = {
            'belong': forms.TextInput(attrs={'placeholder': '소속 학교/ 학원', 'class': 'textinput'}),
            'age': CustomSelect(attrs={'class': 'select', }),
            'strategy': forms.TextInput(attrs={'placeholder': '현재 입시전략, 정시/ 수시/ 수시 종류', 'class': 'textinput'}),
            'problem':forms.Textarea(attrs={'placeholder': '현재 모의고사, 내신 성적 등과 겪는 문제점', 'class': 'textarea'}),
            'want':forms.Textarea(attrs={'placeholder': '바라는 수업 방식, 내용 등', 'class': 'textarea'}),
        }

class ApplicationAdminForm(ModelForm):
    class Meta:
        model = Application
        fields = ('state','updated_at')