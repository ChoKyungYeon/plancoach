from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
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
        profiles = (
            Profile.objects
            .filter(state='abled')
            .annotate(
                num_likes=Count('profile_like'),
                num_consults=Count('teacher__consult_teacher')
            )
            .annotate(total=F('num_likes') + F('num_consults'))
            .order_by('-total', '-num_likes')
        )
        context['profiles_all'] = profiles[:3]
        return context

class ContactView(TemplateView):
    template_name = 'homescreenapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document']=Document.objects.all().first()
        return context

    
class AboutusView(TemplateView):
    template_name = 'homescreenapp/aboutus.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.aboutus_link:
            return redirect(document.aboutus_link)
        return super().get(request, *args, **kwargs)

class TermofuseView(TemplateView):
    template_name = 'homescreenapp/termofuse.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.termofuse_link:
            return redirect(document.termofuse_link)
        return super().get(request, *args, **kwargs)

class RefundView(TemplateView):
    template_name = 'homescreenapp/refund.html'


class PrivacypolicyView(TemplateView):
    template_name = 'homescreenapp/privacypolicy.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.privacypolicy_link:
            return redirect(document.privacypolicy_link)
        return super().get(request, *args, **kwargs)

