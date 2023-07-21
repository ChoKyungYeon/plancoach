from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, RedirectView, TemplateView
from applicationapp.decorators import application_create_decorater
from plancoach.updaters import *
from refusalapp.models import Refusal
from applicationapp.forms import ApplicationCreateForm
from applicationapp.models import Application
from plancoach.sms import Send_SMS


@method_decorator(login_required, name='dispatch')
@method_decorator(user_updater, name='dispatch')
class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationCreateForm
    template_name = 'applicationapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = CustomUser.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        student = self.request.user
        teacher = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        with transaction.atomic():
            #form instance
            form.instance.student = student
            form.instance.teacher = teacher
            form.instance.updated_at = datetime.now()
            form.instance.save()
            # object 지우기
            Application.objects.filter(student=student).delete()
            Refusal.objects.filter(student=student).delete()
            # sendsms
            content = f'{student.userrealname} 학생이 수업을 신청했습니다. 신청서를 확인해주세요'
            Send_SMS(teacher.username, content, teacher.can_receive_notification)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('applicationapp:result')

@method_decorator(login_required, name='dispatch')
@method_decorator(application_updater, name='dispatch')
@method_decorator(application_create_decorater, name='dispatch')
class ApplicationDeleteView(DeleteView):
    model = Application
    context_object_name = 'target_application'
    template_name = 'applicationapp/delete.html'

    def get_success_url(self):
        if self.request.user.state == 'teacher':
            return reverse_lazy('teacherapp:dashboard', kwargs={'pk': self.object.teacher.pk})
        else:
            return reverse_lazy('accountapp:studentdguide', kwargs={'pk': self.object.student.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(application_updater, name='dispatch')
class ApplicationUpdateView(UpdateView):
    model = Application
    form_class = ApplicationCreateForm
    context_object_name = 'target_application'
    template_name = 'applicationapp/update.html'

    def get_success_url(self):
        return reverse_lazy('applicationapp:detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(application_updater, name='dispatch')
class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = 'target_application'
    template_name = 'applicationapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state'] = self.object.state
        return context


class ApplicationStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        application = Application.objects.get(pk=self.request.GET.get('application_pk'))
        return reverse('teacherapp:applicationlist', kwargs={'pk': application.teacher.pk})

    def get(self, request, *args, **kwargs):
        application = Application.objects.get(pk=self.request.GET.get('application_pk'))
        student = application.student
        with transaction.atomic():
            # application 상태 변경
            application.state = 'matching'
            application.updated_at = datetime.now()
            application.save()
            # sendsms
            content = '신청서가 수락되었습니다. 연락처를 확인하고 시범 수업을 진행해주세요.'
            Send_SMS(student.username, content, student.can_receive_notification)
            return super(ApplicationStateUpdateView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
@method_decorator(request_user_updater, name='dispatch')
class ApplicationGuideView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'applicationapp/guide.html'

@method_decorator(login_required, name='dispatch')
@method_decorator(request_user_updater, name='dispatch')
class ApplicationResultView(TemplateView):
    model = CustomUser
    template_name = 'applicationapp/result.html'
