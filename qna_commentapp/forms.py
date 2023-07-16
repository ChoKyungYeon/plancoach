from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from qna_commentapp.models import Qna_comment


class Qna_commentCreateForm(ModelForm):
    class Meta:
        model = Qna_comment
        fields = ('image','content')
        labels = {
            'content':'댓글 내용',
            'image':'댓글 이미지',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '댓글 내용을 작성해주세요', 'class': 'textarea-wide'}),
            'image':  forms.FileInput(attrs={'placeholder': '댓글 이미지', 'class': 'fileinput'}),
        }
