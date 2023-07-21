from django import forms

from documentapp.models import Document


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document

        fields = ( 'termofuse', 'privacypolicy', 'kakaotalk',  'termofuse_updated',
                  'privacypolicy_updated')

        labels = {
            'termofuse': '이용약관',
            'privacypolicy': '개인정보 처리 방침',
            'kakaotalk': '카카오톡 링크',
            'termofuse_updated': '이용약관 수정일',
            'privacypolicy_updated': '개인정보 처리 방침 수정일',
        }

        widgets = {
            'termofuse': forms.FileInput(attrs={'class': 'fileinput'}),
            'privacypolicy': forms.FileInput(attrs={'class': 'fileinput'}),
            'termofuse_updated': forms.DateInput(attrs={'type': 'date', 'class': 'dateinput'}),
            'privacypolicy_updated': forms.DateInput(attrs={'type': 'date', 'class': 'dateinput'}),
        }