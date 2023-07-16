from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from consult_qnaapp.forms import Consult_qnaCreateForm
from consult_qnaapp.models import Consult_qna
from consultapp.models import Consult
from qna_likeapp.models import Qna_like


class Consult_qnaCreateView(CreateView):
    model = Consult_qna
    form_class = Consult_qnaCreateForm
    template_name = 'consult_qnaapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult=get_object_or_404(Consult, pk=self.kwargs['pk'])
        context['target_consult'] = target_consult
        return context

    def form_valid(self, form):
        target_consult=get_object_or_404(Consult, pk=self.kwargs['pk'])
        with transaction.atomic():
            form.instance.consult = target_consult
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consult_qnaapp:detail', kwargs={'pk': self.object.pk})



class Consult_qnaListView(DetailView):
    model = Consult
    context_object_name = 'target_consult'
    template_name = 'consult_qnaapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_consult=get_object_or_404(Consult, pk=self.kwargs['pk'])
        qnas=target_consult.consult_qna.all().order_by('-created_at')
        target_student=target_consult.student
        qnas_like = qnas.filter(qna_like__student=target_student)
        qnas_answered = qnas.filter(is_answered =True)
        qnas_unanswered = qnas.exclude(id__in=qnas_answered)
        qnas_length=len(qnas)
        qnas_answered_length=len(qnas_answered)
        ratio =int(round(qnas_answered_length/qnas_length*100)) if qnas else 0
        context['qnas_like'] = qnas_like
        context['qnas_unanswered'] = qnas_unanswered
        context['qnas_answered'] = qnas_answered
        context['qnas'] = qnas
        context['qnas_answered_length'] = qnas_answered_length
        context['qnas_length'] = qnas_length
        context['ratio'] = ratio
        return context


class Consult_qnaUpdateView(UpdateView):
    model = Consult_qna
    form_class = Consult_qnaCreateForm
    context_object_name = 'target_consult_qna'
    template_name = 'consult_qnaapp/update.html'


    def get_success_url(self):
        return reverse_lazy('consult_qnaapp:detail', kwargs={'pk': self.object.pk})


class Consult_qnaDetailView(DetailView):
    model = Consult_qna
    context_object_name = 'target_consult_qna'
    template_name = 'consult_qnaapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_qna=get_object_or_404(Consult_qna, pk=self.kwargs['pk'])
        target_consult = target_qna.consult
        qna_next = Consult_qna.objects.filter(consult=target_consult, created_at__gt=target_qna.created_at).order_by(
            'created_at').first()
        qna_before = Consult_qna.objects.filter(consult=target_consult, created_at__lt=target_qna.created_at).order_by(
            '-created_at').first()
        like = Qna_like.objects.filter(student=target_consult.student,
                                            consult_qna=target_qna).first()
        context['like']=like
        context['qna_next'] = qna_next
        context['qna_before'] = qna_before
        context['comments'] = target_qna.qna_comment.all()
        context['target_qna'] = target_qna
        context['target_consult'] = target_consult
        return context
