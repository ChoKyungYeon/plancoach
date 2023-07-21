from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm
from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm
from accountapp.models import CustomUser


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
                self.add_error('username', '')  # Add field-level error.
                self.add_error('password', '잘못된 전화번호 또는 비밀번호입니다.')  # Add field-level error.
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class AccountCreateForm(UserCreationForm):
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
            'placeholder': "확인을 위해 위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput feild-nolabel',
            'autocomplete': 'new-password'
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'userrealname', 'password1', 'password2')
        labels = {
            'email': '이메일',
            'userrealname': '사용자 실명',
        }

        widgets = {
            'userrealname': forms.TextInput(attrs={'placeholder': '실명을 입력하세요', 'class': 'textinput', }),
            'email': forms.EmailInput(attrs={'placeholder': '수업 결제 영수증이 입력한 이메일로 전송됩니다', 'class': 'textinput', }),
        }


class AccountInfoUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'userrealname')
        labels = {
            'email': '이메일',
            'userrealname': '사용자 실명',
        }

        widgets = {
            'userrealname': forms.TextInput(attrs={'placeholder': '실명을 입력하세요', 'class': 'textinput', }),
            'email': forms.EmailInput(attrs={'placeholder': '수업 결제 영수증이 입력한 이메일로 전송됩니다', 'class': 'textinput', }),
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
            'placeholder': "확인을 위해 위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput feild-nolabel',
            'autocomplete': 'new-password'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')


class AccountAdminForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('state',)
        labels = {
            'state': '계정 상태',
        }
