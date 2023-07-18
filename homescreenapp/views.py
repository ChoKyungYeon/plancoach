from django.views.generic import TemplateView
from documentapp.models import Document


class HomescreenView(TemplateView):
    template_name = 'homescreenapp/homescreen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['target_step'] = self.request.user.student_step()
        else:
            context['target_step'] = 'unauthenticated'
        return context


class ContactView(TemplateView):
    template_name = 'homescreenapp/contact.html'


class AboutusView(TemplateView):
    template_name = 'homescreenapp/aboutus.html'


class TermofuseView(TemplateView):
    template_name = 'homescreenapp/termofuse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_document = Document.objects.all().first()
        context['target_document'] = target_document
        return context


class RefundView(TemplateView):
    template_name = 'homescreenapp/refund.html'


class PrivacypolicyView(TemplateView):
    template_name = 'homescreenapp/privacypolicy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_document = Document.objects.all().first()
        context['target_document'] = target_document
        return context
