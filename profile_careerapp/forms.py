
from django import forms
from django.forms import ModelForm

from profile_careerapp.models import Profile_career
from plancoach.widgets import  CustomSelect



class Profile_careerCreateForm(ModelForm):

    class Meta:
        model = Profile_career
        fields = ('year','duration','subject','type','content')
        labels = {
            'year':'시작 년도',
            'duration':'지속 기간',
            'content':'교습 내용',
            'subject':'교습 과목',
            'type':'교습 종류',
        }

        widgets = {
            'year':CustomSelect(attrs={ 'class': 'select',}),
            'duration':CustomSelect(attrs={ 'class': 'select',}),
            'type': forms.TextInput(attrs={'placeholder': '과외/조교/문제 제작등', 'class': 'textinput'}),
            'content': forms.TextInput(attrs={'placeholder': '고등학교 3학년 내신& 수능 대비', 'class': 'textinput'}),
            'subject': CustomSelect(attrs={ 'class': 'select',}),
        }
