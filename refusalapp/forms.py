from django import forms
from django.forms import ModelForm

from refusalapp.models import Refusal


class RefusalCreateForm(ModelForm):

    class Meta:
        model = Refusal
        fields = ('content',)
        labels = {
            'content':'거절 사유 작성',
        }
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': '거절 사유', 'class': 'textinput'}),
        }
