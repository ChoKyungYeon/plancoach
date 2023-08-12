from django import forms
from django.forms import ModelForm
from consult_feedbackapp.models import Consult_feedback

class Consult_feedbackCreateForm(ModelForm):
    class Meta:
        model = Consult_feedback
        fields = ('classtime', 'subjects')
        labels = {
            'subjects': '대상 과목',
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
            'content': '학생 종합 분석 및 과제',
        }

        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': '1 공부법 및 학습 조언 2 학생 시험, 성적 분석 3 교재 및 강의 4 기타 사항 등', 'class': 'textarea-wide'}),
        }

class Consult_feedbackTodoUpdateForm(ModelForm):
    class Meta:
        model = Consult_feedback
        fields = ('todo',)
        labels = {
            'todo': '종합 학습 플랜',
        }

        widgets = {
            'todo': forms.Textarea(
                attrs={'placeholder': '전체 과목별 학습 시간 및 분량, 교재/인강 학습 범위 작성. 필요시 요일별 상세 플랜 작성', 'class': 'textarea-wide'}),
        }
