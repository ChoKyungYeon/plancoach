
from django import forms
from django.forms import ModelForm

from profile_careerapp.models import Profile_career
from plancoach.widgets import  CustomSelect



class Profile_careerCreateForm(ModelForm):

    class Meta:
        model = Profile_career
        fields = ('year','duration','subject','type','content')
        labels = {
            'year':'활동 시기',
            'duration':'기간',
            'content':'활동 내용',
            'subject':'과목',
            'type':'교습 종류',
        }

        widgets = {
            'year':CustomSelect(attrs={ 'class': 'select',}),
            'duration':CustomSelect(attrs={ 'class': 'select',}),
            'type': forms.TextInput(attrs={'placeholder': '개인 교습, 학원 조교, 문제 제작 등', 'class': 'textinput'}),
            'content': forms.TextInput(attrs={'placeholder': '활동 기관, 대상, 내용 등', 'class': 'textinput'}),
            'subject': CustomSelect(attrs={ 'class': 'select',}),
        }
