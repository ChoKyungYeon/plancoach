from django.forms import ModelForm
from django import forms
from profile_introductionapp.models import Profile_introduction


class Profile_introductionCreateForm(ModelForm):

    class Meta:
        model = Profile_introduction
        fields = ('content',)
        labels = {
            'content':'한 줄 소개',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '본인의 강점을 드러낼 수 있는 짧은 설명', 'class': 'textarea'}),
        }
