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
            'gpaverificationimage':'성적 증명',

        }

        widgets = {
            'schooltype': CustomSelect(attrs={'placeholder': '', 'class': 'select'}),
            'highschool': forms.TextInput(attrs={'placeholder': '000고등학교', 'class': 'textinput'}),
            'score':forms.Textarea(attrs={'placeholder': '고교 성적 및 활동', 'class': 'textarea'}),
            'gpaverificationimage': forms.FileInput(attrs={'placeholder': '증빙 자료', 'class': 'fileinput'}),

        }
