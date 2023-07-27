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
            'image':'질문 이미지',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 작성해주세요','class': 'textinput'}),
            'content': forms.Textarea(attrs={'placeholder': '질문 작성 이후 삭제가 불가능합니다.', 'class': 'textarea-wide'}),
            'image':  forms.FileInput(attrs={'class': 'fileinput'}),
        }
