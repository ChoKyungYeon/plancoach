from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView
from consult_qnaapp.models import Consult_qna
from qna_commentapp.decorators import *
from qna_commentapp.forms import Qna_commentCreateForm
from qna_commentapp.models import Qna_comment
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Qna_commentCreateDecorator, name='dispatch')
class Qna_commentCreateView(CreateView):
    model = Qna_comment
    form_class = Qna_commentCreateForm
    template_name = 'qna_commentapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_qna=get_object_or_404(Consult_qna, pk=self.kwargs['pk'])
        context['target_qna'] = target_qna
        return context

    def form_valid(self, form):
        target_qna=get_object_or_404(Consult_qna, pk=self.kwargs['pk'])
        target_user=self.request.user
        with transaction.atomic():
            # form instacne
            form.instance.consult_qna= target_qna
            form.instance.customuser= self.request.user
            form.instance.save()
            if target_user == target_qna.consult.teacher:
                target_qna.is_answered = True
                target_qna.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consult_qnaapp:detail', kwargs={'pk': self.object.consult_qna.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Qna_commentUpdateDecorator, name='dispatch')
class Qna_commentUpdateView(UpdateView):
    model = Qna_comment
    form_class = Qna_commentCreateForm
    context_object_name = 'target_qna_comment'
    template_name = 'qna_commentapp/update.html'
    def get_success_url(self):
        return reverse_lazy('consult_qnaapp:detail', kwargs={'pk': self.object.consult_qna.pk})



