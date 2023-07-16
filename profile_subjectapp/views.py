from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from plancoach.decorators import is_teacher
from profile_subjectapp.decorators import profile_subject_ownership_required
from profile_subjectapp.forms import Profile_subjectCreateForm
from profile_subjectapp.models import Profile_subject
from profileapp.models import Profile


class Profile_subjectCreateView(CreateView):
    model = Profile_subject
    form_class = Profile_subjectCreateForm
    template_name = 'profile_subjectapp/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        target_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        kwargs['target_profile'] = target_profile
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['target_profile'] = target_profile
        return context

    def form_valid(self, form):
        target_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = target_profile
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.kwargs['pk']})


class Profile_subjectUpdateView(UpdateView):
    model = Profile_subject
    context_object_name = 'target_profile_subject'
    form_class = Profile_subjectCreateForm
    template_name = 'profile_subjectapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})


class Profile_subjectDeleteView(DeleteView):
    model =Profile_subject
    context_object_name = 'target_profile_subject'
    template_name = 'profile_subjectapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})
