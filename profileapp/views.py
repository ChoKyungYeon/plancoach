from datetime import datetime

from django.db import transaction
from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, RedirectView, TemplateView, DeleteView
from accountapp.models import CustomUser
from plancoach.choice import subjectchoice, schoolyearchoice
from profile_bankapp.models import Profile_bank
from plancoach.sms import Send_SMS
from profile_consulttypeapp.models import Profile_consulttype
from profile_likeapp.models import Profile_like
from profile_scholarshipapp.models import Profile_scholarship
from profileapp.forms import ProfileTuitionUpdateForm, ProfileCreateForm
from profileapp.models import Profile
from teacherapplyapp.models import Teacherapply
from plancoach.updaters import *
from django.utils.decorators import method_decorator

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
                content='합격 수기 작성',
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
                content='수업 소개 작성'
            )
            teacherapply.delete()
            # sendsms
            content = '선생님 프로필이 생성 되었습니다. 프로필을 완성하고 대시보드에서 활성화하세요!'
            Send_SMS( target_user.username, content,  target_user.can_receive_notification)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')


class ProfileDeleteView(DeleteView):
    model =Profile
    context_object_name = 'target_profile'
    template_name = 'profileapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')



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



#모두 확인 가능
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
        sats=getattr(target_profile, 'profile_sat', None).order_by('satyear').all()
        context['scholarship'] =getattr(target_profile, 'profile_scholarship', None)
        context['careers'] = getattr(target_profile, 'profile_career', None).order_by('year').all().all()
        context['sats'] = sats
        context['gpa'] = getattr(target_profile, 'profile_gpa', None)
        context['subjects'] = subjects
        context['consulttype'] = getattr(target_profile, 'profile_consulttype', None)
        context['schoolyear_length'] = int(datetime.now().date().strftime("%y")) + 2 - 12
        context['can_add_subject'] = len(subjectchoice) != len(subjects)
        context['can_add_sat'] = len(schoolyearchoice) != len(sats)
        context['tuition'] = str(target_profile.tuition)[:2]
        return context

#모두 확인 가능)
class ProfileListView(TemplateView):
    model = Profile
    template_name = 'profileapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.request.user
        profiles = (
            Profile.objects
            .filter(state='abled')
            .annotate(
                num_likes=Count('profile_like'),
                num_consults=Count('teacher__consult_teacher')
            )
            .annotate(total=F('num_likes') + F('num_consults'))
            .order_by('-total', '-num_likes')
        )

        context['profiles_all'] = profiles
        if target_user.is_authenticated:
            profiles_like = profiles.filter(profile_like__student=target_user)
            context['profiles_like'] = profiles_like

        profiles_dict = {'정시': [], '내신': [], '학생부': [], '중등': []}

        for profile in profiles:
            for consulttype in profile.profile_consulttype.consulttype:
                if consulttype in profiles_dict:
                    profiles_dict[consulttype].append(profile)

        context['profiles_sat'] = profiles_dict['정시']
        context['profiles_gpa'] = profiles_dict['내신']
        context['profiles_extra'] = profiles_dict['학생부']
        context['profiles_middelschool'] = profiles_dict['중등']
        return context





class ProfileStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('teacherapp:dashboard', kwargs={'pk': self.request.GET.get('user_pk')})
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.request.GET.get('user_pk'))
        profile = Profile.objects.get(teacher=user)
        profile.state = 'abled' if profile.state == 'disabled' else 'disabled'
        profile.save()
        return super(ProfileStateUpdateView, self).get(request, *args, **kwargs)

