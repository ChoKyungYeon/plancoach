from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from accountapp.models import CustomUser
from consultapp.models import Consult
from plancoach.variables import current_date
from profileapp.models import Profile
from refundapp.models import Refund
from salaryapp.models import Salary
from teacherapplyapp.models import Teacherapply


# Create your views here.

#1 로그인  3슈퍼유저
class SuperuserDashboardView(TemplateView):
    model = CustomUser
    template_name = 'superuserapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.all().order_by('teacher__int_username')
        context['profiles'] = profiles
        context['salarys'] = Salary.objects.filter(is_given=False, salaryday__lte=current_date+timedelta(days=90))
        print(Salary.objects.filter(is_given=False).first().salaryday)
        context['refunds'] = Refund.objects.filter(is_given=False)
        context['teacherapplys'] = Teacherapply.objects.all()
        return context

