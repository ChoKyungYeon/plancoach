from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DeleteView
from consult_feedbackapp.models import Consult_feedback
from feedback_coachapp.decorators import *
from feedback_coachapp.forms import Feedback_coachCreateForm, Feedback_coachUpdateForm
from feedback_coachapp.models import Feedback_coach
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Feedback_coachCreateDecorator, name='dispatch')
class Feedback_coachCreateView(CreateView):
    model = Feedback_coach
    form_class = Feedback_coachCreateForm
    template_name = 'feedback_coachapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        context['target_feedback'] = target_feedback
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        target_feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        kwargs['target_feedback'] = target_feedback
        return kwargs

    def form_valid(self, form):
        target_feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        with transaction.atomic():
            form.instance.consult_feedback = target_feedback
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:coachdetail', kwargs={'pk': self.object.consult_feedback.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Feedback_coachUpdateDecorator, name='dispatch')
class Feedback_coachUpdateView(UpdateView):
    model = Feedback_coach
    form_class = Feedback_coachUpdateForm
    context_object_name = 'target_feedback_coach'
    template_name = 'feedback_coachapp/update.html'

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:coachdetail', kwargs={'pk': self.object.consult_feedback.pk})


@method_decorator(login_required, name='dispatch')
@method_decorator(Feedback_coachDeleteDecorator, name='dispatch')
class Feedback_coachDeleteView(DeleteView):
    model = Feedback_coach
    context_object_name = 'target_feedback_coach'
    template_name = 'feedback_coachapp/delete.html'

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:coachdetail', kwargs={'pk': self.object.consult_feedback.pk})
