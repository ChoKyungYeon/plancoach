from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from profile_gpaapp.models import Profile_gpa



class Profile_gpaCreateForm(ModelForm):

    class Meta:
        model = Profile_gpa
        fields = ( 'highschool','schooltype','score','gpaverificationimage')
        labels = {
            'highschool': '출신 고등학교',
            'schooltype': '고등학교 분류',
            'score':'고교 성적 및 활동',
            'gpaverificationimage':'성적 증명 (선택)',

        }

        widgets = {
            'schooltype': CustomSelect(attrs={'placeholder': '', 'class': 'select'}),
            'highschool': forms.TextInput(attrs={'placeholder': '00고등학교', 'class': 'textinput'}),
            'score':forms.Textarea(attrs={'placeholder': '1 고등학교 내신 2 생활 기록부 3 활동 및 수상 경력 등 ', 'class': 'textarea'}),
            'gpaverificationimage': forms.FileInput(attrs={ 'class': 'fileinput'}),

        }
