from django.urls import reverse_lazy
from django.views.generic import UpdateView
from feedback_planapp.forms import Feedback_planUpdateForm
from feedback_planapp.models import Feedback_plan


class Feedback_planUpdateView(UpdateView):
    model = Feedback_plan
    form_class = Feedback_planUpdateForm
    context_object_name = 'target_feedback_plan'
    template_name = 'feedback_planapp/update.html'

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:plandetail', kwargs={'pk': self.object.consult_feedback.pk})
