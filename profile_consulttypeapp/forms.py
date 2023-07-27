from django import forms
from django.forms import ModelForm

from plancoach.choice import consulttypechoice
from plancoach.utils import update_field_choices
from plancoach.widgets import CustomSelect
from profile_consulttypeapp.models import Profile_consulttype

class Profile_consulttypeCreateForm(ModelForm):


    class Meta:
        model = Profile_consulttype
        fields = ('consulttype', 'content')
        labels = {
            'consulttype': '가능 컨설팅',
            'content': '컨설팅 소개',
        }
        widgets = {
            'consulttype': forms.CheckboxSelectMultiple(attrs={ 'class': 'selectmultiple'}),
            'content': forms.Textarea(attrs={'placeholder': '1 대상 학생 2 본인의 수업 방식 3 자신만의 노하우/차별점 ', 'class': 'textarea'}),
        }
