from datetime import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from accountapp.models import CustomUser
from consultapp.forms import ConsultCreateForm, ConsultInfoUpdateForm
from consultapp.models import Consult
from feedback_planapp.models import Feedback_plan
from plancoach.sms import Send_SMS
from paymentapp.models import Payment
from profileapp.models import Profile
from plancoach.updaters import *
from django.utils.decorators import method_decorator

class ConsultCreateView(CreateView):
    model = Consult
    form_class = ConsultCreateForm
    template_name = 'consultapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        student = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        application = student.application_student
        teacher = self.request.user
        with transaction.atomic():
            # form valid
            form.instance.teacher = teacher
            form.instance.student = student
            form.instance.age = application.age
            form.instance.belong = application.belong
            form.instance.want = application.want
            form.instance.strategy = application.strategy
            form.instance.problem = application.problem
            form.instance.tuition = teacher.profile.tuition
            form.instance.save()
            # object delete
            application.delete()
            # sendsms
            content = '신규 수업이 생성되었습니다. 입금을 완료하고 수업을 시작하세요!'
            Send_SMS(student.username, content, student.can_receive_notification)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapp:applicationlist', kwargs={'pk': self.object.teacher.pk})


class ConsultInfoUpdateView(UpdateView):
    model = Consult
    context_object_name = 'target_consult'
    form_class = ConsultInfoUpdateForm
    template_name = 'consultapp/infoupdate.html'

    def get_success_url(self):
        return reverse_lazy('consultapp:dashboard', kwargs={'pk': self.object.pk})


class ConsultDashboardView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consultapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult = self.object
        target_consult_classlink = getattr(target_consult, 'consult_classlink', None)
        target_classlink = target_consult_classlink.link if target_consult_classlink else None
        teacher = target_consult.teacher

        qnas = target_consult.consult_qna.all().order_by('-created_at')
        qnas_unanswered = qnas.filter(is_answered=False)
        qnas_length = len(qnas)
        qnas_unanswered_length = len(qnas_unanswered)
        today = datetime.now().date()
        feedbacks = target_consult.consult_feedback.all()

        today_plan = Feedback_plan.objects.filter(consult_feedback__in=feedbacks, plantime=today).order_by(
            '-created_at').first()
        context['qnas_answered_length'] = qnas_unanswered_length
        context['qnas_length'] = qnas_length
        context['feedbacks_length'] = len(feedbacks)
        context['today_plan'] = today_plan if today_plan and today_plan.content else None

        context['profile'] = Profile.objects.get(teacher=teacher)
        context['target_consult_classlink'] = target_consult_classlink
        context['target_classlink'] = target_classlink
        context['payments'] = Payment.objects.filter(consult=self.object, is_paid_ok=True).order_by(
            '-created_at').count()
        return context


class ConsultApplyDetailView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consultapp/applydetail.html'


class ConsultPaymentListView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consultapp/paymentlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.filter(consult=self.object, is_paid_ok=True).order_by('-created_at')
        return context
