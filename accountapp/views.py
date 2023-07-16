from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, RedirectView
from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountLoginForm, AccountCreateForm,AccountInfoUpdateForm ,AccountPasswordUpdateForm
from accountapp.models import CustomUser
from accountapp.updaters import target_user_updater
from accountapp.utils import user_step_calculator
from applicationapp.models import Application
from applicationapp.utils import teacher_application_classification
from consultapp.models import Consult
from plancoach.updaters import request_user_updater
from phonenumberapp.models import Phonenumber
from profileapp.models import Profile
from profileapp.utils import profile_completeness_calculator
from refundapp.models import Refund
from teacherapplyapp.models import Teacherapply

has_qualification = [account_ownership_required, login_required]
#@method_decorator(has_qualification, 'get')


'''1로그인 required-x
 '''
class AccountLoginView(LoginView):
    form_class = AccountLoginForm
    template_name = 'accountapp/login.html'
    success_url = reverse_lazy('homescreenapp:homescreen')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homescreenapp:homescreen')
        return super().dispatch(request, *args, **kwargs)

'''1로그인 required-x
5 pk관련 조건- phonenumber
'''
class AccountCreateView(CreateView):
    model = CustomUser
    form_class = AccountCreateForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_phonenumber']= get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        with transaction.atomic():
            target_phonenumber = get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
            phone=target_phonenumber.phonenumber
            temp_user = form.save(commit=False)
            temp_user.username = phone
            temp_user.int_username = int(phone)
            temp_user.save()
            target_phonenumber.delete()
            return super().form_valid(form)



# 1 비로그인조건 X 2 선생조건 소유자 3 3학생조건 소유자 4슈퍼유저 조건 소유자 5pk 조건x

class AccountInfoUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class= AccountInfoUpdateForm
    template_name = 'accountapp/infoupdate.html'
    def get_success_url(self):
        return reverse_lazy('accountapp:setting', kwargs={'pk':self.object.pk})


# 1 비로그인조건 X 2 선생조건 소유자 3 3학생조건 소유자 4슈퍼유저 조건 소유자 5pk 조건x
class AccountPasswordUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class= AccountPasswordUpdateForm
    success_url= reverse_lazy('accountapp:logout')
    template_name = 'accountapp/passwordupdate.html'

# 1 비로그인조건 X 2 선생조건 소유자 3 3학생조건 소유자 4슈퍼유저 조건 소유자 5pk 조건x
class AccountPasswordResetView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class= AccountPasswordUpdateForm
    success_url= reverse_lazy('accountapp:logout')
    template_name = 'accountapp/passwordreset.html'

# 1 비로그인조건 X 2 선생조건 소유자 3 3학생조건 소유자 4슈퍼유저 조건 소유자 5pk 조건x
class AccountDeleteView(DeleteView):
    model = CustomUser
    context_object_name = 'target_user'
    success_url= reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'



# 1 비로그인조건 X 2 선생조건 소유자 3 3학생조건 소유자 4슈퍼유저 조건 소유자 5pk 조건x
class AccountSettingView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/setting.html'









#1 로그인 2 소유자
class AccountNotificationUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accountapp:setting', kwargs={'pk': self.request.GET.get('user_pk')})

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.request.GET.get('user_pk'))
        user.can_receive_notification = True if user.can_receive_notification==False else False
        user.save()
        return super(AccountNotificationUpdateView, self).get(request, *args, **kwargs)
