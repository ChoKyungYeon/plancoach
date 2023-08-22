from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from qna_commentapp.models import Qna_comment


class Qna_commentCreateForm(ModelForm):
    class Meta:
        model = Qna_comment
        fields = ('image','content')
        labels = {
            'content':'답변 내용',
            'image':'답변 이미지',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '답변 작성 이후 삭제가 불가능합니다.', 'class': 'textarea-wide textarea-comment'}),
            'image':  forms.FileInput(attrs={ 'class': 'fileinput'}),
        }
