from django import forms
from django.forms import ModelForm
from consult_feedbackapp.models import Consult_feedback

class Consult_feedbackCreateForm(ModelForm):
    class Meta:
        model = Consult_feedback
        fields = ('classtime', 'subjects')
        labels = {
            'subjects': '피드백 과목',
            'classtime': '수업 일자',
        }

        widgets = {
            'subjects': forms.CheckboxSelectMultiple(attrs={'class': 'selectmultiple'}),
            'classtime': forms.DateInput(attrs={'placeholder': '구체적 시간 입력', 'type': 'date', 'class': 'dateinput'}),
        }


class Consult_feedbackUpdateForm(ModelForm):
    class Meta:
        model = Consult_feedback
        fields = ('classtime',)
        labels = {
            'classtime': '수업 일자',
        }

        widgets = {
            'classtime': forms.DateInput(attrs={'placeholder': '구체적 시간 입력', 'type': 'date', 'class': 'dateinput'}),
        }


class Consult_feedbackContentUpdateForm(ModelForm):
    class Meta:
        model = Consult_feedback
        fields = ('content',)
        labels = {
            'content': '학생 종합 분석/ 과제',
        }

        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': '분석: 학생 성적, 분석, 방향성 , 과제: 구매할 교재, 강의 등', 'class': 'textarea-wide'}),
        }
