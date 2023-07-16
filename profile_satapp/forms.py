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
            'satyear':'응시 학년도 ( 내신 성적 기입시 공백 )',
            'score':'성적 기입' ,
            'satverificationimage':'성적 증명',

        }

        widgets = {
            'satyear': CustomSelect(attrs={ 'class': 'select',}),
            'score':forms.Textarea(attrs={'placeholder': '원점수 위주로 기입 예시) 국어-언매:00점, 수학-미적분:00점', 'class': 'textarea'}),
            'satverificationimage': forms.FileInput(attrs={'class': 'fileinput', 'value': '파일 선택'}),

        }
