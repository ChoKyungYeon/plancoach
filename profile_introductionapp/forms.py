from django.forms import ModelForm
from django import forms
from profile_introductionapp.models import Profile_introduction


class Profile_introductionCreateForm(ModelForm):

    class Meta:
        model = Profile_introduction
        fields = ('content',)
        labels = {
            'content':'한줄소개',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '자기소개', 'class': 'textarea'}),
        }
