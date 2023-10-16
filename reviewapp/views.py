from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, TemplateView, DeleteView

from qna_commentapp.forms import Qna_commentCreateForm
from reviewapp.decorators import *
from reviewapp.forms import ReviewCreateForm, ReviewManageForm
from reviewapp.models import Review


# Create your views here.

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(ReviewCreateDecorator, name='dispatch')
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'reviewapp/create.html'

    def form_valid(self, form):
        target_user=self.request.user
        target_consult = target_user.consult_student
        with transaction.atomic():
            form.instance.customuser = target_user
            form.instance.userrealname= target_user.userrealname
            form.instance.age= target_consult.age
            form.instance.created_at= datetime.now().date()
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reviewapp:list')

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(ReviewManageDecorator, name='dispatch')
class ReviewManageView(CreateView):
    model = Review
    form_class = ReviewManageForm
    template_name = 'reviewapp/manage.html'

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.customuser= self.request.user
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reviewapp:list')



@method_decorator(never_cache, name='dispatch')
@method_decorator(ReviewListDecorator, name='dispatch')
class ReviewListView(TemplateView):
    model = Review
    template_name = 'reviewapp/list.html'

    def get_context_data(self, **kwargs):
        target_user=self.request.user
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all().order_by('-created_at')
        context['can_review'] = target_user.can_review() if target_user.is_authenticated else False
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(ReviewDeleteDecorator, name='dispatch')
class ReviewDeleteView(DeleteView):
    model = Review
    context_object_name = 'target_review'
    template_name = 'reviewapp/delete.html'

    def get_success_url(self):
        return reverse_lazy('reviewapp:list')
