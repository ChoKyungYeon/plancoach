from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, RedirectView

from accountapp.decorators import *
from accountapp.forms import AccountLoginForm, AccountCreateForm, AccountInfoUpdateForm, AccountPasswordUpdateForm
from accountapp.models import CustomUser
from phonenumberapp.models import Phonenumber
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
class AccountLoginView(LoginView):
    form_class = AccountLoginForm
    template_name = 'accountapp/login.html'
    success_url = reverse_lazy('homescreenapp:homescreen')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homescreenapp:homescreen')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(never_cache, name='dispatch')
@method_decorator(AccountCreateDecorator, name='dispatch')
class AccountCreateView(CreateView):
    model = CustomUser
    form_class = AccountCreateForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_phonenumber'] = get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        phonenumber = get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        phone = phonenumber.phonenumber
        agree_terms = form.cleaned_data['agree_terms']
        with transaction.atomic():
            if not agree_terms == True:
                form.add_error('agree_terms', '약관 및 방침에 동의해 주세요')
                return self.form_invalid(form)
            form.instance.username= phone
            form.instance.save()
            phonenumber.delete()
            return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnerDecorator, name='dispatch')
class AccountInfoUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountInfoUpdateForm
    template_name = 'accountapp/infoupdate.html'

    def get_success_url(self):
        return reverse_lazy('accountapp:setting', kwargs={'pk': self.object.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnerDecorator, name='dispatch')
class AccountPasswordUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountPasswordUpdateForm
    success_url = reverse_lazy('accountapp:logout')
    template_name = 'accountapp/passwordupdate.html'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnerDecorator, name='dispatch')
class AccountPasswordResetView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountPasswordUpdateForm
    success_url = reverse_lazy('accountapp:logout')
    template_name = 'accountapp/passwordreset.html'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountDeleteDecorator, name='delete')
@method_decorator(AccountGetDeleteDecorator, name='get')
class AccountDeleteView(DeleteView):
    model = CustomUser
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnerDecorator, name='dispatch')
class AccountSettingView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/setting.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(AccountNotificationUpdateDecorator, name='dispatch')
class AccountNotificationUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accountapp:setting', kwargs={'pk': self.request.GET.get('user_pk')})

    def get(self, request, *args, **kwargs):
        target_user = CustomUser.objects.get(pk=self.request.GET.get('user_pk'))
        target_user.can_receive_notification = True if target_user.can_receive_notification == False else False
        target_user.save()
        return super(AccountNotificationUpdateView, self).get(request, *args, **kwargs)
