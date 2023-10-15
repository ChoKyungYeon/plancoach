from django.db import transaction
from django.shortcuts import render
from django.views.generic import CreateView

from qna_commentapp.forms import Qna_commentCreateForm
from reviewapp.forms import ReviewCreateForm
from reviewapp.models import Review


# Create your views here.

