from django import forms
from django.forms import ModelForm

from consult_qnaapp.models import Consult_qna

class Consult_qnaCreateForm(ModelForm):
    class Meta:
        model = Consult_qna
        fields = ('image','title','content')
        labels = {
            'title':'질문 제목',
            'content':'질문 내용',
            'image':'문제 이미지',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 작성해주세요','class': 'textinput'}),
            'content': forms.Textarea(attrs={'placeholder': '질문 내용을 작성해주세요', 'class': 'textarea-wide'}),
            'image':  forms.FileInput(attrs={'placeholder': '문제 이미지', 'class': 'fileinput'}),
        }
