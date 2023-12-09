from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from accountapp.models import CustomUser
from depositapp.models import Deposit
from documentapp.models import Document
from homescreenapp.models import Pageview
from paymentapp.models import Payment
from profileapp.models import Profile
from refundapp.models import Refund
from salaryapp.models import Salary
from superuserapp.decorators import SuperuserDashboardDecorator
from teacherapplyapp.models import Teacherapply
from django.utils.decorators import method_decorator

#1 로그인  3슈퍼유저
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(SuperuserDashboardDecorator, name='dispatch')
class SuperuserDashboardView(TemplateView):
    template_name = 'superuserapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.annotate(username_as_int=Cast('teacher__username', IntegerField())).order_by('username_as_int')
        context['profiles'] = profiles
        context['salarys'] = Salary.objects.filter(is_given=False, salaryday__lte=datetime.now().date())
        context['refunds'] = Refund.objects.filter(is_given=False)
        context['payments'] = Payment.objects.filter(is_paid_ok=False)
        context['teacherapplys'] = Teacherapply.objects.filter(is_done=True)
        context['document'] = Document.objects.all().first()
        context['deposit'] = Deposit.objects.all().first()
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(SuperuserDashboardDecorator, name='dispatch')
class SuperuserPageviewView(TemplateView):
    template_name = 'superuserapp/pageview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageviews'] = Pageview.objects.order_by('-date')
        today=datetime.now().date()
        total_user=CustomUser.objects.exclude(state='superuser')
        total_stundet=total_user.filter(state='student')
        total_teacher=total_user.filter(state='teacher')
        context['increased_teacher_today'] = total_teacher.filter(signup_at=today).count()
        context['increased_student_today'] = total_stundet.filter(signup_at=today).count()
        context['total_student'] = total_stundet.count()
        context['total_teacher'] = total_teacher.count()
        context['today'] = today
        return context

