from django import forms

from plancoach.widgets import CustomSelect
from profileapp.models import Profile


class ProfileCreateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('teacher',)
        labels = {
            # your labels here
        }
        widgets = {
            'teacher': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].required = False


class ProfileTuitionUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('tuition',)
        labels = {
            'tuition':'',
        }
        widgets = {
            'tuition': CustomSelect(attrs={ 'class': 'select',}),
        }
