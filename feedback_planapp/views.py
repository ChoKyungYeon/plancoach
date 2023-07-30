from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, RedirectView

from feedback_planapp.decorators import *
from feedback_planapp.forms import Feedback_planUpdateForm
from feedback_planapp.models import Feedback_plan


@method_decorator(login_required, name='dispatch')
@method_decorator(Feedback_planUpdateDecorator, name='dispatch')
class Feedback_planUpdateView(UpdateView):
    model = Feedback_plan
    form_class = Feedback_planUpdateForm
    context_object_name = 'target_feedback_plan'
    template_name = 'feedback_planapp/update.html'

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:plandetail', kwargs={'pk': self.object.consult_feedback.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(Feedback_planStateUpdateDecorator, name='dispatch')
class Feedback_planStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        plan = Feedback_plan.objects.get(pk=self.request.GET.get('plan_pk'))
        return reverse('consult_feedbackapp:plandetail', kwargs={'pk': plan.consult_feedback.pk})

    def get(self, request, *args, **kwargs):
        plan = Feedback_plan.objects.get(pk=self.request.GET.get('plan_pk'))
        plan.is_done = True if plan.is_done == False else False
        plan.save()
        return super(Feedback_planStateUpdateView, self).get(request, *args, **kwargs)
