from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from profile_careerapp.forms import Profile_careerCreateForm
from profile_careerapp.models import Profile_career
from profileapp.models import Profile
from plancoach.updaters import *
from django.utils.decorators import method_decorator

class Profile_careerCreateView(CreateView):
    model = Profile_career
    form_class = Profile_careerCreateForm
    template_name = 'profile_careerapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_profile=get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['target_profile'] = target_profile
        return context

    def form_valid(self, form):
        target_profile=get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile=target_profile
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.kwargs['pk']})

class Profile_careerDeleteView(DeleteView):
    model = Profile_career
    context_object_name = 'target_profile_career'
    template_name = 'profile_careerapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})


class Profile_careerUpdateView(UpdateView):
    model = Profile_career
    form_class = Profile_careerCreateForm
    context_object_name = 'target_profile_career'
    template_name = 'profile_careerapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})
