from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView
from accountapp.models import CustomUser
from plancoach.utils import profile_completeness_calculator, salaryday_calculator
from django.utils.decorators import method_decorator

from teacherapp.decorators import *

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherDashboardDecorator, name='dispatch')
class TeacherDashboardView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'teacherapp/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.object
        target_profile= target_user.profile
        profiles_liked = target_profile.profile_like.count()
        profiles_completed, profiles_uncompleted, ratio= profile_completeness_calculator(target_user)
        applications=self.object.application_teacher.all()
        context['target_profile'] = target_profile
        context['target_bank'] = target_profile.profile_bank
        context['profiles_liked'] = profiles_liked
        context['consults_ongoing'] = target_user.consult_teacher.all()
        context['applications_applied']=applications.filter(state='applied')
        context['applications_matching']=applications.filter(state='matching')
        context['profiles_completed']=profiles_completed
        context['profiles_uncompleted']=profiles_uncompleted
        context['profile_completeness']=ratio
        context['salary_length'] = len(self.object.salary.filter(is_given=True))
        context['target_salary']= target_user.salary.filter(salaryday=salaryday_calculator(datetime.now().date())).first()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherDashboardDecorator, name='dispatch')
class TeacherSalaryListView(DetailView):
    model = CustomUser
    template_name = 'teacherapp/salarylist.html'
    context_object_name = 'target_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salarys'] = self.object.salary.filter(is_given=True)
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherDashboardDecorator, name='dispatch')
class TeacherApplicationListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'teacherapp/applicationlist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications=self.object.application_teacher.all()
        context['applications_applied']=applications.filter(state='applied')
        context['applications_matching']=applications.filter(state='matching')
        return context
