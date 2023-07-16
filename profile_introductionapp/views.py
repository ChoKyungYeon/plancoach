from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from plancoach.decorators import is_teacher
from profile_introductionapp.decorators import profile_introduction_ownership_required
from profile_introductionapp.forms import Profile_introductionCreateForm
from profile_introductionapp.models import Profile_introduction
from profileapp.models import Profile


class Profile_introductionCreateView(CreateView):
    model = Profile_introduction
    form_class = Profile_introductionCreateForm
    template_name = 'profile_introductionapp/create.html'

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

class Profile_introductionUpdateView(UpdateView):
    model = Profile_introduction
    context_object_name = 'target_profile_introduction'
    form_class = Profile_introductionCreateForm
    template_name = 'profile_introductionapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})



class Profile_introductionDeleteView(DeleteView):
    model = Profile_introduction
    context_object_name = 'target_profile_introduction'
    template_name = 'profile_introductionapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})
