from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from accountapp.models import CustomUser
from documentapp.models import Document
from feedback_likeapp.decorators import Feedback_likeDecorator
from homescreenapp.decorators import *
from homescreenapp.models import Pageview
from profileapp.models import Profile
from reviewapp.models import Review
from django.db.models.fields import Field

@method_decorator(HomescreenDecorator, name='dispatch')
class HomescreenView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        today = datetime.now().date()
        for field in CustomUser._meta.get_fields():
            if isinstance(field, Field):  # 필드 중에서 실제 데이터베이스 필드만 출력
                print(field.name, field.get_internal_type())
        pageview = Pageview.objects.filter(date=today).first()
        if not pageview:
            pageview = Pageview.objects.create(date=today)

        if not request.session.get('is_checked', None):
            pageview.count += 1
            pageview.save()
            request.session['is_checked'] = True

        return super().dispatch(request, *args, **kwargs)

    template_name = 'homescreenapp/homescreen.html'
    def get_context_data(self, **kwargs):
        target_user = self.request.user
        context = super().get_context_data(**kwargs)
        context['document'] = Document.objects.all().first()
        context['target_month'] = datetime.now().month
        context['reviews'] = Review.objects.all().order_by('created_at')[:4]
        context['can_teacherapply'] = not target_user.is_authenticated or \
                                      (target_user.state == 'student' and target_user.student_step() in ['initial', 'end'])
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


class ClassdetailView(TemplateView):
    template_name = 'homescreenapp/classdetail.html'