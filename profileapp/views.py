from datetime import date

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, RedirectView, TemplateView, DeleteView

from accountapp.models import CustomUser
from accountapp.utils import user_step_calculator
from plancoach.choice import subjectchoice, schoolyearchoice
from plancoach.variables import current_date
from profile_bankapp.models import Profile_bank
from plancoach.sms import Send_SMS

from profile_consulttypeapp.models import Profile_consulttype
from profile_likeapp.models import Profile_like
from profile_scholarshipapp.models import Profile_scholarship
from profileapp.decorators import profile_ownership_required
from profileapp.forms import ProfileTuitionUpdateForm, ProfileCreateForm
from profileapp.models import Profile
from teacherapplyapp.models import Teacherapply


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profileapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_teacherapply=get_object_or_404(Teacherapply, pk=self.kwargs['pk'])
        context['target_teacherapply'] = target_teacherapply
        return context

    def form_valid(self, form):
        target_teacherapply=get_object_or_404(Teacherapply, pk=self.kwargs['pk'])
        target_user=target_teacherapply.customuser
        with transaction.atomic():
            form.instance.teacher = target_user
            target_user.state ='teacher'
            target_user.save()
            form.instance.save()
            target_teacherapply.delete()
            Profile_scholarship.objects.create(profile=form.instance, accepttype=target_teacherapply.accepttype,
                                               studentid=target_teacherapply.studentid, content='합격 수기 작성',
                                               schoolverificationimage=target_teacherapply.schoolimage,
                                               school=target_teacherapply.school,
                                               major=target_teacherapply.major)
            Profile_bank.objects.create(profile=form.instance, bank=target_teacherapply.bank,
                                       accountnumber=target_teacherapply.accountnumber,depositor=target_teacherapply.depositor)
            Profile_consulttype.objects.create(profile=form.instance,consulttype=target_teacherapply.consulttype,
                                               content='수업 소개 작성')
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
            temp_profile = form.save(commit=False)
            temp_profile.payment_updated_at = current_date
            temp_profile.save()
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
        target_step, target_consult_pk =user_step_calculator(target_user)
        can_user_apply= target_step =='step1' or target_step =='denied'
        like = Profile_like.objects.filter(student=target_user, profile=target_profile).first() if target_step != 'unauthenticated' else None
        subjects=getattr(target_profile, 'profile_subject', None).all()
        sats=getattr(target_profile, 'profile_sat', None).order_by('satyear').all()
        context['like']=like
        context['scholarship'] =getattr(target_profile, 'profile_scholarship', None)
        context['careers'] = getattr(target_profile, 'profile_career', None).order_by('year').all().all()
        context['sats'] = sats
        context['gpa'] = getattr(target_profile, 'profile_gpa', None)
        context['subjects'] = subjects
        context['consulttype'] = getattr(target_profile, 'profile_consulttype', None)
        context['can_user_apply'] = can_user_apply
        context['schoolyear_length'] = int(current_date.strftime("%y")) + 2 - 12
        context['can_add_subject'] = len(subjectchoice) != len(subjects)
        context['can_add_sat'] = len(schoolyearchoice) != len(sats)
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

        profiles_dict = {'정시': [], '내신': [], '학생부': [], '논술': []}

        for profile in profiles:
            for consulttype in profile.profile_consulttype.consulttype:
                if consulttype in profiles_dict:
                    profiles_dict[consulttype].append(profile)

        context['profiles_sat'] = profiles_dict['정시']
        context['profiles_gpa'] = profiles_dict['내신']
        context['profiles_extra'] = profiles_dict['학생부']
        context['profiles_essay'] = profiles_dict['논술']
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

