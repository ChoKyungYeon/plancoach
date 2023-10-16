from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from reviewapp.models import Review


class ReviewCreateForm(ModelForm):
    class Meta:
        model = Review
        fields = ('image','content')
        labels = {
            'content':'후기 작성',
            'image':'첨부 이미지',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '작성 이후 삭제할 수 없으며 이름은 성까지만 노출됩니다.',
                                             'class': 'textarea'}),
            'image':  forms.FileInput(attrs={ 'class': 'fileinput'}),
        }

class ReviewManageForm(ModelForm):
    class Meta:
        model = Review
        fields = ('userrealname','age','image','content','created_at')
        labels = {
            'userrealname':'작성자명',
            'age':'작성자 나이',
            'created_at': '후기 작성일',
            'content':'후기 작성',
            'image':'첨부 이미지',
        }

        widgets = {
            'userrealname': forms.TextInput(attrs={'placeholder': '작성자 이름', 'class': 'textinput', }),
            'content': forms.Textarea(attrs={'placeholder': '후기 내용',
                                             'class': 'textarea'}),
            'image':  forms.FileInput(attrs={ 'class': 'fileinput'}),
            'age': CustomSelect(attrs={'class': 'select', }),
            'created_at': forms.DateInput(attrs={'placeholder': '구체적 시간 입력', 'type': 'date', 'class': 'dateinput'}),
        }
