from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView

from consult_feedbackapp.decorators import *
from consult_feedbackapp.forms import Consult_feedbackCreateForm, Consult_feedbackUpdateForm, \
    Consult_feedbackContentUpdateForm
from consult_feedbackapp.models import Consult_feedback
from consult_feedbackapp.utils import planatime_calulator
from consultapp.models import Consult
from feedback_coachapp.models import Feedback_coach
from feedback_likeapp.models import Feedback_like
from feedback_planapp.models import Feedback_plan
from plancoach.choice import subjectchoice
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_feedbackCreateDecorator, name='dispatch')
class Consult_feedbackCreateView(CreateView):
    model = Consult_feedback
    form_class = Consult_feedbackCreateForm
    template_name = 'consult_feedbackapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        context['target_consult'] = target_consult
        return context

    def form_valid(self, form):
        consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        classtimes = consult.consult_feedback.values_list('classtime', flat=True)
        classtime = form.cleaned_data['classtime']
        with transaction.atomic():
            # form error
            if classtime > datetime.now().date():
                form.add_error('classtime', '수업 기록은 수업 진행 이후에 등록해 주세요')
                return self.form_invalid(form)
            elif classtime in classtimes:
                form.add_error('classtime', '이미 등록된 수업 일자입니다')
                return self.form_invalid(form)
            # form intance
            form.instance.consult = consult
            form.instance.save()
            # create objects
            for subject in form.cleaned_data['subjects']:
                Feedback_coach.objects.create(
                    consult_feedback=form.instance,
                    subject=subject
                )
            for date in planatime_calulator(classtime):
                Feedback_plan.objects.create(consult_feedback=form.instance, plantime=date)

            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:coachdetail', kwargs={'pk': self.object.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_feedbackListDecorator, name='dispatch')
class Consult_feedbackListView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consult_feedbackapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        feedbacks = target_consult.consult_feedback.all().order_by('-classtime')
        target_classlink = getattr(target_consult, 'consult_classlink', None)
        target_student = target_consult.student
        feedbacks_like = feedbacks.filter(feedback_like__student=target_student)
        context['feedbacks_like'] = feedbacks_like
        context['feedbacks'] = feedbacks
        context['target_classlink'] = target_classlink
        context['latest_feedback'] = feedbacks.first()
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_feedbackDeleteDecorator, name='dispatch')
class Consult_feedbackDeleteView(DeleteView):
    model = Consult_feedback
    context_object_name = 'target_consult_feedback'
    template_name = 'consult_feedbackapp/delete.html'

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:list', kwargs={'pk': self.object.consult.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_feedbackUpdateDecorator, name='dispatch')
class Consult_feedbackUpdateView(UpdateView):
    model = Consult_feedback
    form_class = Consult_feedbackUpdateForm
    context_object_name = 'target_consult_feedback'
    template_name = 'consult_feedbackapp/update.html'

    def form_valid(self, form):
        feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        consult = feedback.consult
        classtimes = consult.consult_feedback.values_list('classtime', flat=True)
        plans = feedback.feedback_plan.all().order_by('plantime')
        classtime = form.cleaned_data['classtime']
        with transaction.atomic():
            # form invalid
            if classtime > datetime.now().date():
                form.add_error('classtime', '수업 기록은 수업 후에 등록해 주세요')
                return self.form_invalid(form)
            elif classtime in classtimes:
                form.add_error('classtime', '이미 등록된 수업 일자입니다')
                return self.form_invalid(form)
            # form valid
            form.instance.save()
            # object update
            for plan, date in zip(plans, planatime_calulator(classtime)):
                plan.plantime = date
                plan.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:coachdetail', kwargs={'pk': self.object.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_feedbackContentUpdateDecorator, name='dispatch')
class Consult_feedbackContentUpdateView(UpdateView):
    model = Consult_feedback
    form_class = Consult_feedbackContentUpdateForm
    context_object_name = 'target_consult_feedback'
    template_name = 'consult_feedbackapp/contentupdate.html'

    def get_success_url(self):
        return reverse_lazy('consult_feedbackapp:coachdetail', kwargs={'pk': self.object.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_feedbackBaseDetailDecorator, name='dispatch')
class ConsultFeedbackBaseDetailView(DetailView):
    model = Consult_feedback
    context_object_name = 'target_consult_feedback'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        target_consult = target_feedback.consult
        feedback_next = Consult_feedback.objects.filter(consult=target_consult,
                                                        classtime__gt=target_feedback.classtime).order_by(
            'classtime').first()
        feedback_before = Consult_feedback.objects.filter(consult=target_consult,
                                                          classtime__lt=target_feedback.classtime).order_by(
            '-classtime').first()
        like = Feedback_like.objects.filter(student=target_consult.student,
                                            consult_feedback=target_feedback).first()
        context['like'] = like
        context['feedback_next'] = feedback_next
        context['feedback_before'] = feedback_before
        context['target_feedback'] = target_feedback
        context['target_consult'] = target_consult
        return context


class Consult_feedbackPlanDetailView(ConsultFeedbackBaseDetailView):
    template_name = 'consult_feedbackapp/plandetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        plans = target_feedback.feedback_plan.all().order_by('plantime')
        context['plans'] = plans
        return context


class Consult_feedbackCoachDetailView(ConsultFeedbackBaseDetailView):
    template_name = 'consult_feedbackapp/coachdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_feedback = get_object_or_404(Consult_feedback, pk=self.kwargs['pk'])
        coaches = target_feedback.feedback_coach.all()
        context['coaches'] = coaches
        context['can_add_coaches'] = len(coaches) != len(subjectchoice)
        return context

