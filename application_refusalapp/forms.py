from django import forms
from django.forms import ModelForm

from application_refusalapp.models import Application_refusal


class Application_refusalCreateForm(ModelForm):

    class Meta:
        model = Application_refusal
        fields = ('content',)
        labels = {
            'content':'거절 사유 작성',
        }
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': '거절 사유', 'class': 'textinput'}),
        }
