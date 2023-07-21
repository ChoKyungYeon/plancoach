from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth import login
from accountapp.models import CustomUser
from plancoach.sms import Send_SMS
from phonenumberapp.forms import PhonenumberCreateForm, PhoneNumberVerifyForm, PhonenumberUpdateForm
from phonenumberapp.models import Phonenumber
from django.contrib.auth import get_user_model
from plancoach.updaters import *
from django.utils.decorators import method_decorator

class PhonenumberCreateMixin(CreateView):
    model = Phonenumber
    form_class = PhonenumberCreateForm
    def form_valid(self, form):
        for phonenumber in Phonenumber.objects.all():
            phonenumber.updater()
        phonenumber = form.cleaned_data['phonenumber']
        usernames = get_user_model().objects.values_list('username', flat=True)
        with transaction.atomic():
            # form invalid
            if len(phonenumber) <11 or phonenumber[:3] != '010':
                form.add_error('phonenumber', '정확한 전화번호를 입력해주세요')
                return self.form_invalid(form)
            if self.condition(phonenumber, usernames):
                form.add_error('phonenumber', self.error_message)
                return self.form_invalid(form)

            form.instance.verification_code='111111'#deploy check random.randint(100000, 999999)
            form.instance.save()
            to = form.instance.phonenumber
            content = f'{self.sms_message} {form.instance.verification_code}를 입력하세요'
            Send_SMS(to, content, True)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(self.reverse_url, kwargs={'pk': self.object.pk})

    def condition(self, phonenumber, usernames):
        raise NotImplementedError()



class PhonenumberSignupCreateView(PhonenumberCreateMixin):
    template_name = 'phonenumberapp/signupcreate.html'
    reverse_url = 'phonenumberapp:signupverify'
    sms_message = 'Plan & Coach 인증번호'
    error_message = '이미 존재하는 전화번호입니다.'

    def condition(self, phonenumber, usernames):
        return phonenumber in usernames

class PhonenumberUpdateCreateView(PhonenumberCreateMixin):
    form_class = PhonenumberUpdateForm
    template_name = 'phonenumberapp/updatecreate.html'
    reverse_url = 'phonenumberapp:updateverify'
    sms_message = 'Plan & Coach 인증번호'
    error_message = '이미 존재하는 전화번호입니다.'

    def condition(self, phonenumber, usernames):
        return phonenumber in usernames


class PhonenumberSearchCreateView(PhonenumberCreateMixin):
    template_name = 'phonenumberapp/searchcreate.html'
    reverse_url = 'phonenumberapp:searchverify'
    sms_message = 'Plan & Coach 인증번호'
    error_message = '가입되지 않은 전화번호 입니다.'

    def condition(self, phonenumber, usernames):
        return phonenumber not in usernames

#없으면 redirect하도록, 시작할때 업데이트
class PhonenumberVerifyMixin(FormView):
    model = Phonenumber
    form_class = PhoneNumberVerifyForm

    def dispatch(self, request, *args, **kwargs):
        phonenumber= get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        if phonenumber.timeout() <3:
            phonenumber.delete()
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phonenumber= get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        context['phonenumber'] = phonenumber
        context['remaining_time'] = phonenumber.timeout()
        context['redirect_url'] = reverse(self.redirect_url)
        return context

    def form_valid(self, form):
        compare_code = form.cleaned_data['compare_code']
        phonenumber= get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        error_count = phonenumber.error_count
        with transaction.atomic():
            if len(compare_code) < 6:
                form.add_error('compare_code', '인증번호 6자리를 입력해주세요')
                return self.form_invalid(form)

            if phonenumber.verification_code == compare_code:
                self.success_action(phonenumber)
                return HttpResponseRedirect(self.get_success_url())
            else:
                if error_count == 4:
                    phonenumber.delete()
                    return redirect(self.redirect_url)
                    return self.form_invalid(form)
                else:
                    phonenumber.error_count = error_count + 1
                    phonenumber.save()
                    form.add_error('compare_code', f'인증 코드 오류 횟수 ({phonenumber.error_count}/5)')
                    return self.form_invalid(form)

    def success_action(self, phonenumber):
        raise NotImplementedError()


class PhonenumberSignupVerifyView(PhonenumberVerifyMixin):
    template_name = 'phonenumberapp/signupverify.html'
    redirect_url = 'phonenumberapp:signupcreate'

    def get_success_url(self):
        return reverse_lazy('accountapp:create', kwargs={'pk': self.kwargs['pk']})

    def success_action(self, phonenumber):
        phonenumber.is_verified = True
        phonenumber.save()


class PhonenumberSearchVerifyView(PhonenumberVerifyMixin):
    template_name = 'phonenumberapp/searchverify.html'
    redirect_url = 'phonenumberapp:searchcreate'

    def success_action(self, phonenumber):
        phonenumber.is_verified = True
        phonenumber.save()
        user = CustomUser.objects.get(username=phonenumber.phonenumber)
        if user is not None:
            login(self.request, user)
        phonenumber.delete()

    def get_success_url(self):
        return reverse_lazy('accountapp:passwordreset', kwargs={'pk': self.request.user.pk})

class PhonenumberUpdateVerifyView(PhonenumberVerifyMixin):
    template_name = 'phonenumberapp/updateverify.html'
    redirect_url = 'phonenumberapp:updatecreate'

    def success_action(self, phonenumber):
        target_user=self.request.user
        phonenumber.is_verified = True
        phonenumber.save()
        target_user.username = phonenumber.phonenumber
        target_user.save()

    def get_success_url(self):
        return reverse_lazy('accountapp:setting',  kwargs={'pk': self.request.user.pk})

