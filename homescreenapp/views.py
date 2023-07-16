from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from accountapp.utils import user_step_calculator, can_apply_teacher
from documentapp.models import Document


class HomescreenView(TemplateView):
    template_name = 'homescreenapp/homescreen.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        target_step, target_consult_pk =user_step_calculator(user)
        can_user_apply = target_step == 'step1' or target_step == 'denied'
        context['can_user_apply'] = can_user_apply
        context['can_apply_teacher'] = can_apply_teacher(user)
        return context

class ContactView(TemplateView):
    template_name = 'homescreenapp/contact.html'

class AboutusView(TemplateView):
    template_name = 'homescreenapp/aboutus.html'

class TermofuseView(TemplateView):
    template_name = 'homescreenapp/termofuse.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_document=Document.objects.all().first()
        context['target_document'] = target_document
        return context


class RefundView(TemplateView):
    template_name = 'homescreenapp/refund.html'

class TuitionView(TemplateView):
    template_name = 'homescreenapp/tuition.html'

class PrivacypolicyView(TemplateView):
    template_name = 'homescreenapp/privacypolicy.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_document=Document.objects.all().first()
        context['target_document'] = target_document
        return context

