from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, RedirectView, TemplateView
from accountapp.models import CustomUser
from applicationapp.updaters import target_application_updater
from applicationapp.forms import ApplicationCreateForm
from applicationapp.models import Application
from plancoach.sms import Send_SMS
from plancoach.updaters import request_user_updater
from plancoach.variables import current_datetime


#applicationupdator
#1 로그인 3학생 4step 1, pk가 선생님
@method_decorator(request_user_updater, 'get')
class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationCreateForm
    template_name = 'applicationapp/create.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = CustomUser.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        user = self.request.user
        with transaction.atomic():
            Application.objects.filter(student=user).delete()
            form.instance.student = user
            form.instance.teacher = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('applicationapp:result')

#1 로그인 2 소유자  4step3
@method_decorator(request_user_updater, 'get')
class ApplicationDeleteView(DeleteView):
    model = Application
    context_object_name = 'target_application'
    template_name = 'applicationapp/delete.html'
    def get_success_url(self):
        if self.request.user.state == 'teacher':
            return reverse_lazy('teacherapp:dashboard', kwargs={'pk': self.object.teacher.pk})
        else:
            return reverse_lazy('accountapp:studentdguide', kwargs={'pk': self.object.student.pk})

#1 로그인 2 소유자  4step3
#applicationupdator
@method_decorator(request_user_updater, 'get')
#@method_decorator(is_qualified, 'get')
@method_decorator(request_user_updater, 'post')
#@method_decorator(is_qualified, 'post')
class ApplicationUpdateView(UpdateView):
    model = Application
    form_class = ApplicationCreateForm
    context_object_name = 'target_application'
    template_name = 'applicationapp/update.html'
    def get_success_url(self):
        return reverse_lazy('applicationapp:detail', kwargs={'pk': self.object.pk})

#1 로그인 2 소유자(학생,선생) 3슈퍼유저
@method_decorator(target_application_updater, 'get')
class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = 'target_application'
    template_name = 'applicationapp/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state'] = self.object.state
        context['phonenumber_reveal'] = self.object.state in ['matching', 'waiting', 'ongoing']

        return context

#1 로그인 2 소유자(선생만) 4step3
@method_decorator(request_user_updater, 'get')
class ApplicationStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        application = Application.objects.get(pk=self.request.GET.get('application_pk'))
        user=application.student
        content = '신청서가 수락되었습니다. 연락처를 확인하고 시범 수업을 진행해주세요.'
        Send_SMS(user.username, content, user.can_receive_notification)
        return reverse('teacherapp:applicationlist', kwargs={'pk': application.teacher.pk})

    def get(self, request, *args, **kwargs):
        application = Application.objects.get(pk=self.request.GET.get('application_pk'))
        application.state = 'matching'
        application.updated_at = current_datetime
        application.save()
        return super(ApplicationStateUpdateView, self).get(request, *args, **kwargs)

@method_decorator(request_user_updater, 'get')
class ApplicationStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        application = Application.objects.get(pk=self.request.GET.get('application_pk'))
        user=application.student
        content = '신청서가 수락되었습니다. 연락처를 확인하고 시범 수업을 진행해주세요.'
        Send_SMS(user.username, content, user.can_receive_notification)
        return reverse('teacherapp:applicationlist', kwargs={'pk': application.teacher.pk})

    def get(self, request, *args, **kwargs):
        application = Application.objects.get(pk=self.request.GET.get('application_pk'))
        application.state = 'matching'
        application.updated_at = current_datetime
        application.save()
        return super(ApplicationStateUpdateView, self).get(request, *args, **kwargs)

#1 로그인  3학생만 4step 1
@method_decorator(request_user_updater, 'get')
class ApplicationGuideView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'applicationapp/guide.html'


#1 로그인  3학생 4step3
@method_decorator(request_user_updater, 'get')
class ApplicationResultView(TemplateView):
    model = CustomUser
    template_name = 'applicationapp/result.html'

#1 로그인 2 소유자 3슈퍼유저

