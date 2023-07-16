from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView

from accountapp.models import CustomUser
from accountapp.updaters import target_user_updater
from applicationapp.utils import teacher_application_classification
from plancoach.variables import current_date
from profileapp.utils import profile_completeness_calculator
from salaryapp.models import Salary
from salaryapp.utils import salaryday_calculator


# 1 비로그인조건 X 2 선생조건 소유자 3 3학생조건 소유자 4슈퍼유저 조건 소유자 5pk 조건x
@method_decorator(target_user_updater, 'get')
class TeacherDashboardView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'teacherapp/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.object
        target_profile= target_user.profile
        profiles_liked = target_profile.profile_like.count()
        consults_ongoing = target_user.consult_teacher.all()
        applications_applied, applications_matching, applications_waiting=\
            teacher_application_classification(target_user)

        profiles_completed, profiles_uncompleted, ratio= profile_completeness_calculator(target_user)

        context['target_profile'] = target_profile
        context['target_bank'] = target_profile.profile_bank
        context['profiles_liked'] = profiles_liked
        context['applications_applied']=applications_applied
        context['consults_ongoing'] = consults_ongoing
        context['applications_matching']=applications_matching
        context['applications_waiting']=applications_waiting
        context['applications_ongoing']=len(applications_waiting)+len(applications_matching)
        context['profiles_completed']=profiles_completed
        context['profiles_uncompleted']=profiles_uncompleted
        context['profile_completeness']=ratio
        context['salary_length'] = len(self.object.salary.filter(is_given=True))
        context['target_salary']= target_user.salary.filter(salaryday=salaryday_calculator(current_date+timedelta(days=30))).first()
        return context


class TeacherSalaryListView(DetailView):
    model = CustomUser
    template_name = 'teacherapp/salarylist.html'
    context_object_name = 'target_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salarys'] = self.object.salary.filter(is_given=True)
        return context

@method_decorator(target_user_updater, 'get')
class TeacherApplicationListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'teacherapp/applicationlist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.object
        applications_applied, applications_matching, applications_waiting=\
            teacher_application_classification(target_user)
        context['applications_applied']=applications_applied
        context['applications_matching']=applications_matching
        context['applications_waiting']=applications_waiting
        return context
