from django import forms
from django.forms import ModelForm

from reviewapp.models import Review


class ReviewCreateForm(ModelForm):
    class Meta:
        model = Review
        fields = ('image','content')
        labels = {
            'content':'후기 작성',
            'image':'답변 이미지',
        }

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '작성 이후 삭제할 수 없으며 이름은 성까지만 노출됩니다.',
                                             'class': 'textarea'}),
            'image':  forms.FileInput(attrs={ 'class': 'fileinput'}),
        }
