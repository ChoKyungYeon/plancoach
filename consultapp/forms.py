from django import forms
from consultapp.models import Consult
from plancoach.widgets import CustomSelect


class ConsultCreateForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ('teacher', 'student', 'tuition')
        labels = {
        }
        widgets = {
            'teacher': forms.HiddenInput(),
            'student': forms.HiddenInput(),
            'tuition': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].required = False
        self.fields['student'].required = False
        self.fields['tuition'].required = False


class ConsultInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ('belong', 'age',)
        labels = {
            'belong': '소속',
            'age': '학년/나이',
        }
        widgets = {
            'belong': forms.TextInput(attrs={'placeholder': '소속 학교/ 학원', 'class': 'textinput'}),
            'age': CustomSelect(attrs={'class': 'select', }),
        }


class ConsultAdminForm(forms.ModelForm):
    startdate = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=("Year", "Month", "Day")))

    class Meta:
        model = Consult
        fields = ('student', 'teacher','state','age','belong','tuition')
        labels = {
            'state': '상태',
            'startdate': '시작일',
        }
