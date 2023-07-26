from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from accountapp.models import CustomUser
from refusalapp.models import Refusal
from teacherapplyapp.decorators import *
from teacherapplyapp.forms import TeacherapplyUserimageCreateForm, TeacherapplyBankCreateForm, \
    TeacherapplySchoolimageCreateForm, TeacherapplyInfoCreateForm
from teacherapplyapp.models import Teacherapply
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplySchoolimageCreateDecorater, name='dispatch')
class TeacherapplySchoolimageCreateView(CreateView):
    model = Teacherapply
    form_class = TeacherapplySchoolimageCreateForm
    template_name = 'teacherapplyapp/schoolimagecreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        context['target_user'] = target_user
        return context

    def form_valid(self, form):
        target_user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        with transaction.atomic():
            if hasattr(target_user, 'teacherapply'):
                target_user.teacherapply.delete()
            form.instance.customuser = target_user
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapplyapp:userimagecreate', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyBankCreateDecorater, name='dispatch')
class TeacherapplyBankCreateView(UpdateView):
    model = Teacherapply
    form_class = TeacherapplyBankCreateForm
    context_object_name = 'target_teacherapply'
    template_name = 'teacherapplyapp/bankcreate.html'

    def form_valid(self, form):
        form.instance.has_bank = True
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapplyapp:infocreate', kwargs={'pk':self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyUserimageCreateDecorater, name='dispatch')
class TeacherapplyUserimageCreateView(UpdateView):
    model = Teacherapply
    form_class = TeacherapplyUserimageCreateForm
    template_name = 'teacherapplyapp/userimagecreate.html'
    context_object_name = 'target_teacherapply'

    def form_valid(self, form):
        form.instance.has_userimage = True
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapplyapp:bankcreate', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyInfoCreateDecorater, name='dispatch')
class TeacherapplyInfoCreateView(UpdateView):
    model = Teacherapply
    form_class = TeacherapplyInfoCreateForm
    template_name = 'teacherapplyapp/infocreate.html'
    context_object_name = 'target_teacherapply'

    def form_valid(self, form):
        with transaction.atomic():
            Refusal.objects.filter(student=self.object.customuser).delete()
            form.instance.is_done = True
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('studentapp:dashboard', kwargs={'pk': self.object.customuser.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyGuideDecorater, name='dispatch')
class TeacherapplyGuideView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'teacherapplyapp/guide.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyDeleteDecorater, name='dispatch')
class TeacherapplyDeleteView(DeleteView):
    model = Teacherapply
    context_object_name = 'target_teacherapply'
    template_name = 'teacherapplyapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyDetailDecorater, name='dispatch')
class TeacherapplyDetailView(DetailView):
    model = Teacherapply
    context_object_name = 'target_teacherapply'
    template_name = 'teacherapplyapp/detail.html'

@method_decorator(login_required, name='dispatch')
@method_decorator(TeacherapplyRegisterDecorater, name='dispatch')
class TeacherapplyRegisterView(DetailView):
    model = Teacherapply
    context_object_name = 'target_teacherapply'
    template_name = 'teacherapplyapp/register.html'
