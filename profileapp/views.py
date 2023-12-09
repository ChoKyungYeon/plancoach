from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DetailView, RedirectView, TemplateView, DeleteView
from accountapp.models import CustomUser
from plancoach.choice import subjectchoice, schoolyearchoice
from profile_bankapp.models import Profile_bank
from plancoach.sms import Send_SMS
from profile_consulttypeapp.models import Profile_consulttype
from profile_likeapp.models import Profile_like
from profile_scholarshipapp.models import Profile_scholarship
from profileapp.decorators import *
from profileapp.forms import ProfileTuitionUpdateForm, ProfileCreateForm
from profileapp.models import Profile
from teacherapplyapp.models import Teacherapply
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(ProfileCreateDecorator, name='dispatch')
class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profileapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherapply=get_object_or_404(Teacherapply, pk=self.kwargs['pk'])
        context['target_teacherapply'] = teacherapply
        return context

    def form_valid(self, form):
        teacherapply=get_object_or_404(Teacherapply, pk=self.kwargs['pk'])
        target_user=teacherapply.customuser
        with transaction.atomic():
            # form instance
            form.instance.teacher = target_user
            form.instance.save()
            # user modify
            target_user.state ='teacher'
            target_user.save()
            # teacherapply delete
            Profile_scholarship.objects.create(
                profile=form.instance,
                accepttype=teacherapply.accepttype,
                studentid=teacherapply.studentid,
                schoolverificationimage=teacherapply.schoolimage,
                school=teacherapply.school,
                major=teacherapply.major
            )
            Profile_bank.objects.create(
                profile=form.instance,
                bank=teacherapply.bank,
                accountnumber=teacherapply.accountnumber,
                depositor=teacherapply.depositor
            )
            Profile_consulttype.objects.create(
                profile=form.instance,
                consulttype=teacherapply.consulttype,
            )
            teacherapply.delete()
            # sendsms
            content = '선생님 등록이 완료되었습니다. 프로필을 완성하고 웹에서 활성화하세요!'
            Send_SMS( target_user.username, content,  target_user.can_receive_notification)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')

@method_decorator(login_required, name='dispatch')
@method_decorator(ProfileDeleteDecorator, name='dispatch')
class ProfileDeleteView(DeleteView):
    model =Profile
    context_object_name = 'target_profile'
    template_name = 'profileapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(ProfileTuitionUpdateDecorator, name='dispatch')
class ProfileTuitionUpdateView(UpdateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileTuitionUpdateForm
    template_name = 'profileapp/tuitionupdate.html'

    def form_valid(self, form):
        with transaction.atomic():
            self.object.payment_updated_at = datetime.now().date()
            self.object.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacherapp:dashboard', kwargs={'pk': self.object.teacher.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(ProfileDetailDecorator, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'target_profile'
    template_name = 'profileapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_profile=self.object
        target_user = self.request.user
        if self.request.user.is_authenticated:
            like = Profile_like.objects.filter(student=target_user, profile=target_profile).first()
            context['like'] = like
        subjects=getattr(target_profile, 'profile_subject', None).all()
        sats=getattr(target_profile, 'profile_sat', None).order_by('-satyear').all()
        context['scholarship'] =getattr(target_profile, 'profile_scholarship', None)
        context['careers'] = getattr(target_profile, 'profile_career', None).order_by('-year').all().all()
        context['sats'] = sats
        context['gpa'] = getattr(target_profile, 'profile_gpa', None)
        context['subjects'] = subjects
        context['consulttype'] = getattr(target_profile, 'profile_consulttype', None)
        context['schoolyear_length'] = int(datetime.now().date().strftime("%y")) + 2 - 12
        context['can_add_subject'] = len(subjectchoice) != len(subjects)
        context['can_add_sat'] = len(schoolyearchoice) != len(sats)
        return context

@method_decorator(never_cache, name='dispatch')
class ProfileListView(TemplateView):
    model = Profile
    template_name = 'profileapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.request.user
        profiles = (
            Profile.objects
            .filter(is_activated=True)
            .annotate(
                num_likes=Count('profile_like'),
                num_consults=Count('teacher__consult_teacher')
            )
            .annotate(total=F('num_likes') + F('num_consults'))
            .order_by(F('is_highlighted').desc(), '-total', '-num_likes')
        )
        profiles_ascend=profiles.order_by(F('is_highlighted').desc(), 'tuition')

        context['profiles_all'] = profiles
        context['profiles_all_ascend'] = profiles_ascend
        if target_user.is_authenticated:
            profiles_like = profiles.filter(profile_like__student=target_user)
            context['profiles_like'] = profiles_like
            context['profiles_like_ascend'] = profiles_like.order_by('tuition')

        profiles_dict = {'정시': [], '내신': [], '학생부': [], '중등': []}
        profiles_dict_ascend = {'정시': [], '내신': [], '학생부': [], '중등': []}

        for profile in profiles:
            for consulttype in profile.profile_consulttype.consulttype:
                if consulttype in profiles_dict:
                    profiles_dict[consulttype].append(profile)

        for profile in profiles_ascend:
            for consulttype in profile.profile_consulttype.consulttype:
                if consulttype in profiles_dict_ascend:
                    profiles_dict_ascend[consulttype].append(profile)

        context['profiles_sat'] = profiles_dict['정시']
        context['profiles_sat_ascend'] = profiles_dict_ascend['정시']
        context['profiles_gpa'] = profiles_dict['내신']
        context['profiles_gpa_ascend'] = profiles_dict_ascend['내신']
        context['profiles_extra'] = profiles_dict['학생부']
        context['profiles_extra_ascend'] = profiles_dict_ascend['학생부']
        context['profiles_middle'] = profiles_dict['중등']
        context['profiles_middle_ascend'] = profiles_dict_ascend['중등']
        return context




@method_decorator(login_required, name='dispatch')
@method_decorator(ProfileStateUpdateDecorator, name='dispatch')
class ProfileStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('teacherapp:dashboard', kwargs={'pk': self.request.GET.get('user_pk')})

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.request.GET.get('user_pk'))
        profile = Profile.objects.get(teacher=user)
        profile.is_activated = False if profile.is_activated else True
        profile.save()
        return super(ProfileStateUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(ProfileHighlightUpdateDecorator, name='dispatch')
class ProfileHighlightUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('teacherapp:dashboard', kwargs={'pk': self.request.GET.get('user_pk')})
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.request.GET.get('user_pk'))
        profile = Profile.objects.get(teacher=user)
        profile.is_highlighted = False if profile.is_highlighted else True
        profile.save()
        return super(ProfileHighlightUpdateView, self).get(request, *args, **kwargs)

