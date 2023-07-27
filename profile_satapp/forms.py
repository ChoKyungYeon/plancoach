from django import forms
from django.forms import ModelForm

from plancoach.utils import update_field_choices
from plancoach.widgets import CustomSelect
from profile_satapp.models import Profile_sat



class Profile_satCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        target_profile = kwargs.pop('target_profile', None)
        super().__init__(*args, **kwargs)
        if target_profile:
            profile_sat = target_profile.profile_sat
            update_field_choices('satyear', profile_sat, self)


    class Meta:
        model = Profile_sat
        fields = ( 'satyear', 'score','satverificationimage')
        labels = {
            'satyear':'응시 학년도',
            'score':'성적 기입' ,
            'satverificationimage':'성적 증명',

        }

        widgets = {
            'satyear': CustomSelect(attrs={ 'class': 'select',}),
            'score':forms.Textarea(attrs={'placeholder': '과목별 원점수, 등급, 백분위 등', 'class': 'textarea'}),
            'satverificationimage': forms.FileInput(attrs={'class': 'fileinput', 'value': '파일 선택'}),

        }
