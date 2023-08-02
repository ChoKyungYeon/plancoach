from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from accountapp.models import CustomUser
from applicationapp.models import Application
from refusalapp.decorators import *
from refusalapp.forms import RefusalCreateForm
from refusalapp.models import Refusal
from django.utils.decorators import method_decorator

from teacherapplyapp.models import Teacherapply

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(RefusalApplicationRefuseDecorator, name='dispatch')
class RefusalApplicationRefuseView(CreateView):
    model = Refusal
    form_class = RefusalCreateForm
    template_name = 'refusalapp/applicationrefuse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_application'] = get_object_or_404(Application, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        target_application = get_object_or_404(Application, pk=self.kwargs['pk'])
        student=target_application.student
        with transaction.atomic():
            # form instacne
            form.instance.student = student
            form.instance.save()
            # application delete
            target_application.delete()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapp:applicationlist', kwargs={'pk': self.request.user.pk})\

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(RefusalTeacherapplyRefuseDecorator, name='dispatch')
class RefusalTeacherapplyRefuseView(CreateView):
    model = Refusal
    form_class = RefusalCreateForm
    template_name = 'refusalapp/teacherapplyrefuse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_teacherapply'] = get_object_or_404(Teacherapply, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        target_teacherapply = get_object_or_404(Teacherapply, pk=self.kwargs['pk'])
        student=target_teacherapply.customuser
        with transaction.atomic():
            # form instacne
            form.instance.student = student
            form.instance.type = 'teacherapply'
            form.instance.save()
            # application delete
            target_teacherapply.delete()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')
