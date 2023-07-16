from django import forms
from django.forms import ModelForm

from plancoach.utils import update_field_choices
from plancoach.widgets import CustomSelect
from feedback_coachapp.models import Feedback_coach


class Feedback_coachCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        target_feedback = kwargs.pop('target_feedback', None)
        super().__init__(*args, **kwargs)
        if target_feedback:
            feedback_coach = target_feedback.feedback_coach
            update_field_choices('subject', feedback_coach, self)

    class Meta:
        model = Feedback_coach
        fields = ('subject','content')
        labels = {
            'subject':'과목',
            'content':'과목 분석',
        }

        widgets = {
            'subject': CustomSelect(attrs={ 'class': 'select'}),
            'content': forms.Textarea(attrs={'placeholder': '성적, 현 문제점, 교재 등', 'class': 'textarea-wide'}),
        }

class Feedback_coachUpdateForm(ModelForm):

    class Meta:
        model = Feedback_coach
        fields = ('content',)
        labels = {
            'content':'과목 분석',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '성적, 현 문제점, 교재 등', 'class': 'textarea-wide'}),
        }
