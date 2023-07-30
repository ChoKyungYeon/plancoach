from django import forms
from django.forms import ModelForm
from feedback_planapp.models import Feedback_plan

class Feedback_planUpdateForm(ModelForm):
    class Meta:
        model = Feedback_plan
        fields = ('content',)
        labels = {
            'content': '학습 계획 작성',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '1 과목별 학습 시간 및 분량 2 교재/인강 학습 범위 3 기타 계획', 'class': 'textarea-wide'}),
        }
