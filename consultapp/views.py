from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import  CreateView, UpdateView
from accountapp.models import CustomUser
from consultapp.forms import ConsultCreateForm, ConsultInfoUpdateForm
from consultapp.models import Consult
from consultapp.updaters import target_consult_updater
from feedback_planapp.models import Feedback_plan
from plancoach.updaters import request_user_updater
from paymentapp.models import Payment
from plancoach.variables import current_date
from profileapp.models import Profile


# 1 비로그인조건 X 2 선생조건 PK의 학생 어플리케이션과 유저 일치 3학생조건 X 4슈퍼유저 조건 X  pk 학생 step4
@method_decorator(request_user_updater, 'get')
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
            form.instance.application = application
            form.instance.teacher = teacher
            form.instance.student = student
            form.instance.age = application.age
            form.instance.belong = application.belong
            form.instance.tuition = teacher.profile.tuition
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapp:applicationlist', kwargs={'pk': self.object.teacher.pk})

# 1 비로그인조건 X 2 선생조건 PK consult 선생 3 3학생조건 X 4슈퍼유저 조건 X 5pk 조건 conusult 진행중
@method_decorator(request_user_updater, 'get')
class ConsultInfoUpdateView(UpdateView):
    model = Consult
    context_object_name = 'target_consult'
    form_class = ConsultInfoUpdateForm
    template_name = 'consultapp/infoupdate.html'
    def get_success_url(self):
        return reverse_lazy('consultapp:dashboard', kwargs={'pk': self.object.pk})

# 1 비로그인조건 X 2 선생조건 PK consult 선생 3 3학생조건 consult학생 4슈퍼유저 조건 o 5pk 조건 x
@method_decorator(target_consult_updater, 'get')
class ConsultDashboardView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consultapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult = self.object
        target_consult_classlink= getattr(target_consult, 'consult_classlink', None)
        target_classlink=target_consult_classlink.link if target_consult_classlink else None
        teacher = target_consult.teacher

        qnas=target_consult.consult_qna.all().order_by('-created_at')
        qnas_unanswered = qnas.filter(is_answered =False)
        qnas_length=len(qnas)
        qnas_unanswered_length=len(qnas_unanswered)
        today=current_date
        feedbacks=target_consult.consult_feedback.all()

        today_plan = Feedback_plan.objects.filter(consult_feedback__in=feedbacks, plantime=today).order_by('-created_at').first()
        target_plan_content= today_plan.content if today_plan and today_plan.content else '오늘 예정된 학습 계획이 없습니다'


        context['qnas_answered_length'] = qnas_unanswered_length
        context['qnas_length'] = qnas_length
        context['feedbacks_length'] = len(feedbacks)
        context['target_plan_content'] = target_plan_content

        context['profile'] = Profile.objects.get(teacher=teacher)
        context['target_consult_classlink'] = target_consult_classlink
        context['target_classlink'] = target_classlink
        context['payments'] = Payment.objects.filter(consult=self.object, is_paid_ok=True).order_by(
            '-created_at').count()
        return context

@method_decorator(request_user_updater, 'get')
class ConsultPaymentListView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consult/paymentlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.filter(consult=self.object, is_paid_ok=True ).order_by('-created_at')
        return context




