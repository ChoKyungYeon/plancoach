from django.forms import DateInput, Select
from django.forms.utils import flatatt
from django.utils.dateparse import parse_date
from datetime import date

from django.forms.widgets import SelectDateWidget



class CustomSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if index == 0:
            option['label'] = '선택'
        return option