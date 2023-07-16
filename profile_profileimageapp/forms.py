from django.forms import ModelForm
from django import forms
from profile_profileimageapp.models import Profile_profileimage


class Profile_profileimageCreateForm(ModelForm):

    class Meta:
        model = Profile_profileimage
        fields = ('image',)
        labels = {
            'image':'프로필 사진',
        }

        widgets = {
            'image': forms.FileInput(attrs={'placeholder': '프로필 이미지', 'class': 'fileinput'}),
        }
