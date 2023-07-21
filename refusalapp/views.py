from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accountapp.models import CustomUser
from refusalapp.forms import RefusalCreateForm
from refusalapp.models import Refusal
from plancoach.updaters import *
from django.utils.decorators import method_decorator


class RefusalCreateView(CreateView):
    model = Refusal
    form_class = RefusalCreateForm
    template_name = 'refusalapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        target_user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        with transaction.atomic():
            # form instacne
            form.instance.student = target_user
            form.instance.save()
            # application delete
            target_user.application_student.delete()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapp:applicationlist', kwargs={'pk': self.request.user.pk})
