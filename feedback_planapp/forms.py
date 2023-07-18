from django import forms
from django.forms import ModelForm
from feedback_planapp.models import Feedback_plan

class Feedback_planUpdateForm(ModelForm):
    class Meta:
        model = Feedback_plan
        fields = ('content',)
        labels = {
            'content': '학습 계획',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '인강, 교재, 내용 등', 'class': 'textarea-wide'}),
        }
