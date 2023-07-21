from django import forms
from django.forms import ModelForm

from plancoach.widgets import CustomSelect
from salaryapp.models import Salary




class SalaryCreateFormAdmin(ModelForm):
    class Meta:
        model = Salary
        fields = ('salaryday', 'teacher','bank','accountnumber','depositor','is_given','given_at')


class SalaryAdminForm(forms.ModelForm):
    class Meta:
        model = Salary
        labels = {
            'is_given': '지급완료',
        }
        fields = ('is_given',)
