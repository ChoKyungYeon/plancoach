from django import forms
from django.forms import ModelForm

from plancoach.utils import update_field_choices
from plancoach.widgets import CustomSelect
from profile_scholarshipapp.models import Profile_scholarship





class Profile_scholarshipManageForm(ModelForm):
    class Meta:
        model = Profile_scholarship
        fields = ('school', 'major','studentid','accepttype', 'schoolverificationimage','content')
        labels = {
            'school':'학교',
            'major':'전공',
            'studentid':'학번',
            'accepttype':'합격 전형',
            'schoolverificationimage':'재학 증명 사진',
            'content':'합격 수기'

        }

        widgets = {
            'schoolverificationimage': forms.FileInput(attrs={'placeholder': '재학증명', 'class': 'fileinput'}),
            'school': CustomSelect(attrs={ 'class': 'select',}),
            'major': forms.TextInput(attrs={'placeholder': 'oo과', 'class': 'textinput'}),
            'studentid': CustomSelect(attrs={ 'class': 'select',}),
            'content': forms.Textarea(
                attrs={'placeholder': '합격 과정/ 어필 차별점 작성', 'class': 'textarea'}),
            'accepttype': forms.TextInput(attrs={'placeholder': '정시/수시 00전형', 'class': 'textinput'}),
        }

class Profile_scholarshipCreateForm(ModelForm):
    class Meta:
        model = Profile_scholarship
        fields = ('content',)
        labels = {
            'content':'합격 수기'
        }
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': '합격 과정/ 어필 차별점 작성', 'class': 'textarea'}),
        }
