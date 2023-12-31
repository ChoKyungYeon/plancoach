from django import forms
from django.forms import ModelForm

from plancoach.utils import update_field_choices
from plancoach.widgets import CustomSelect
from profile_subjectapp.models import Profile_subject


class Profile_subjectCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        target_profile = kwargs.pop('target_profile', None)
        super().__init__(*args, **kwargs)
        if target_profile:
            profile_subject = target_profile.profile_subject
            update_field_choices('subjectclassification', profile_subject, self)

    class Meta:
        model = Profile_subject
        fields = ('subjectclassification','subjectdetail','content',)
        labels = {
            'subjectclassification':'과목',
            'subjectdetail':'과목 상세 (선택)',
            'content': '과목 설명'
        }

        widgets = {
            'subjectclassification': CustomSelect(attrs={'id': 'id_scoretype', 'class': 'select'}),
            'subjectdetail': forms.TextInput(attrs={'placeholder': '과학탐구 1,2 미적분/기하 등','class': 'textinput' }),
            'content': forms.Textarea(attrs={'placeholder': '과목별 강점 요소', 'class': 'textarea'}),
        }
