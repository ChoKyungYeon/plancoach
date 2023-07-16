from datetime import datetime

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from consult_classlinkapp.forms import Consult_classlinkCreateForm
from consult_classlinkapp.models import Consult_classlink
from consultapp.models import Consult


# Create your views here.
class Consult_classlinkCreateView(CreateView):
    model = Consult_classlink
    form_class = Consult_classlinkCreateForm
    template_name = 'consult_classlinkapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult=get_object_or_404(Consult, pk=self.kwargs['pk'])
        context['target_consult'] = target_consult
        return context

    def form_valid(self, form):
        target_consult=get_object_or_404(Consult, pk=self.kwargs['pk'])
        with transaction.atomic():
            form.instance.consult = target_consult
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consultapp:dashboard', kwargs={'pk': self.kwargs['pk']})

class Consult_classlinkUpdateView(UpdateView):
    model = Consult_classlink
    form_class = Consult_classlinkCreateForm
    context_object_name = 'target_consult_classlink'
    template_name = 'consult_classlinkapp/update.html'

    def form_valid(self, form):
        link = form.cleaned_data['link']
        if 'https://meet.google' not in list(link):
            form.add_error('link', '올바른 링크를 입력 해주세요')
            return self.form_invalid(form)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('consultapp:dashboard', kwargs={'pk': self.object.consult.pk})


