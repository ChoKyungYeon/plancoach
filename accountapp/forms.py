from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm
from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm
from accountapp.models import CustomUser
from plancoach.widgets import CustomSelect


class AccountLoginForm(AuthenticationForm):
    username = UsernameField(
        label=(""),
        widget=forms.NumberInput(attrs={
            'placeholder': '전화번호',
            'class': 'textinput account-login-form-username',
            'autofocus': True,
            'oninput': 'this.value = this.value.slice(0, 11);'
        }),
        validators=[MaxLengthValidator(11)],
        max_length=11
    )
    password = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호',
            'class': 'textinput account-login-form-password',
            'autocomplete': 'current-password'
        })
    )
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                self.add_error('username', '')
                self.add_error('password', '잘못된 전화번호 또는 비밀번호입니다.')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class AccountCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=("비밀번호"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput feild-nolabel',
            'autocomplete': 'new-password'
        }),
    )
    class Meta:
        model = CustomUser
        fields = ('userrealname', 'password1', 'password2','agree_terms')
        labels = {
            'userrealname': '사용자 실명',
            'agree_terms': '전체 동의',
        }

        widgets = {
            'userrealname': forms.TextInput(attrs={'placeholder': '실명을 입력하세요', 'class': 'textinput', }),
            'agree_terms': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }


class AccountInfoUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('userrealname',)
        labels = {
            'userrealname': '사용자 실명',
        }

        widgets = {
            'userrealname': forms.TextInput(attrs={'placeholder': '실명을 입력하세요', 'class': 'textinput', }),
        }


class AccountPasswordUpdateForm(UserCreationForm):
    password1 = forms.CharField(
        label=("새 비밀번호 "),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput feild-nolabel',
            'autocomplete': 'new-password'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')


class AccountCreateAdminForm(ModelForm):
    password1 = forms.CharField(
        label=("비밀번호 "),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput feild-nolabel',
            'autocomplete': 'new-password'
        }),
    )
    class Meta:
        model = CustomUser
        fields = ('username','userrealname', 'password1', 'password2')
        labels = {
            'username': '전화번호',
            'userrealname': '실명',
        }
        widgets = {
            'username':forms.NumberInput(attrs={'placeholder': '- 제외 전화번호 11자',
                                     'class': 'textinput', 'oninput': 'this.value = this.value.slice(0, 11);'}),
            'userrealname': forms.TextInput(attrs={'placeholder': '실명을 입력하세요', 'class': 'textinput', }),
        }

class AccountUpdateAdminForm(ModelForm):
    password1 = forms.CharField(
        label=("비밀번호 "),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput feild-nolabel',
            'autocomplete': 'new-password'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].choices = [
            ('student', '학생'),
            ('superuser', '관리자')
        ]

    class Meta:
        model = CustomUser
        fields = ('state','password1', 'password2')
        labels = {
            'state': '계정 상태',
        }
        widgets = {
            'state':CustomSelect(attrs={'class': 'select'}),
        }