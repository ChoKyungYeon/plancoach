from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from documentapp.models import Document
from feedback_likeapp.decorators import Feedback_likeDecorator
from homescreenapp.decorators import *
from profileapp.models import Profile


@method_decorator(HomescreenDecorator, name='dispatch')
class HomescreenView(TemplateView):
    template_name = 'homescreenapp/homescreen.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = Document.objects.all().first()
        return context

class ContactView(TemplateView):
    template_name = 'homescreenapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document']=Document.objects.all().first()
        return context

    

class TermofuseView(TemplateView):
    template_name = 'homescreenapp/termofuse.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.termofuse:
            return redirect(document.termofuse)
        return super().get(request, *args, **kwargs)

class AnnouncementView(TemplateView):
    template_name = 'homescreenapp/announcement.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.announcement:
            return redirect(document.announcement)
        return super().get(request, *args, **kwargs)

class RefundView(TemplateView):
    template_name = 'homescreenapp/refund.html'


class PrivacypolicyView(TemplateView):
    template_name = 'homescreenapp/privacypolicy.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.privacypolicy:
            return redirect(document.privacypolicy)
        return super().get(request, *args, **kwargs)

