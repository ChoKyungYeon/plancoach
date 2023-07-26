from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from consult_feedbackapp.models import Consult_feedback
from feedback_likeapp.decorators import Feedback_likeDecorater
from feedback_likeapp.models import Feedback_like
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
@method_decorator(Feedback_likeDecorater, name='dispatch')
class Feedback_likeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('consult_feedbackapp:coachdetail', kwargs={'pk': self.request.GET.get('feedback_pk')})

    def get(self, request, *args, **kwargs):
        feedback = get_object_or_404(Consult_feedback, pk=self.request.GET.get('feedback_pk'))
        student = self.request.user
        feedback_like = Feedback_like.objects.filter(student=student, consult_feedback=feedback)
        if feedback_like.exists():
            feedback_like.delete()
        else:
            Feedback_like.objects.create(student=student, consult_feedback=feedback)
        return super(Feedback_likeView, self).get(request, *args, **kwargs)
