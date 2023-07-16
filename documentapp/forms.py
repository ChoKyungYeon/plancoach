from django import forms

from documentapp.models import Document


class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('refund', 'termofuse','privacypolicy','kakaotalk','refund_updated','termofuse_updated','privacypolicy_updated')
        labels = {
            'refund': '환불 정책',
            'termofuse': '이용약관',
            'privacypolicy': '개인정보 처리 방침',
            'kakaotalk': '카카오톡',
            'refund_updated': '환불 정책 수정일',
            'termofuse_updated': '이용약관 수정일',
            'privacypolicy_updated': '개인정보 처리 방침 수정일',
        }