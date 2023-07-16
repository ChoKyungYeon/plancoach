from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from datetime import datetime, timedelta, date

from accountapp.updaters import target_user_updater
from applicationapp.models import Application
from plancoach.sms import Send_SMS
from plancoach.updaters import request_user_updater
from application_refusalapp.forms import Application_refusalCreateForm
from application_refusalapp.models import Application_refusal


@method_decorator(request_user_updater, 'get')
class Application_refusalCreateView(CreateView):
    model = Application_refusal
    form_class = Application_refusalCreateForm
    template_name = 'application_refusalapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_application'] = get_object_or_404(Application, pk=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        with transaction.atomic():
            temp_application_refusal= form.save(commit=False)
            target_application=get_object_or_404(Application, pk=self.kwargs['pk'])
            temp_application_refusal.application =target_application
            temp_application_refusal.save()
            return super().form_valid(form)

    def get_success_url(self):
        target_application = get_object_or_404(Application, pk=self.kwargs['pk'])
        return reverse_lazy('teacherapp:applicationlist', kwargs={'pk': target_application.teacher.pk})





