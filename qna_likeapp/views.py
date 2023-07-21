from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from consult_qnaapp.models import Consult_qna
from qna_likeapp.models import Qna_like
from plancoach.updaters import *
from django.utils.decorators import method_decorator
# Create your views here.


class Qna_likeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('consult_qnaapp:detail', kwargs={'pk':self.request.GET.get('qna_pk')})

    def get(self, request, *args, **kwargs):
        qna=get_object_or_404(Consult_qna, pk=self.request.GET.get('qna_pk'))
        student=self.request.user
        qna_like = Qna_like.objects.filter(student=student, consult_qna=qna)

        if qna_like.exists():
            qna_like.delete()
        else:
            Qna_like.objects.create(student=student, consult_qna=qna)
        return super(Qna_likeView, self).get(request, *args, **kwargs)


