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
            'consulttype': '가능 담당 수업',
            'content': '수업 소개',
        }
        widgets = {
            'consulttype': forms.CheckboxSelectMultiple(attrs={ 'class': 'selectmultiple'}),
            'content': forms.Textarea(attrs={'placeholder': '컨설팅 대상 및 수업 방법 소개', 'class': 'textarea'}),
        }
