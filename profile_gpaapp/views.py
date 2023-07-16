from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView

from plancoach.decorators import is_teacher
from profile_gpaapp.decorators import profile_gpa_ownership_required
from profile_gpaapp.forms import Profile_gpaCreateForm
from profile_gpaapp.models import Profile_gpa
from profileapp.models import Profile


class Profile_gpaCreateView(CreateView):
    model = Profile_gpa
    form_class = Profile_gpaCreateForm
    template_name = 'profile_gpaapp/create.html'

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

class Profile_gpaDeleteView(DeleteView):
    model = Profile_gpa
    context_object_name = 'target_profile_gpa'
    template_name = 'profile_gpaapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})


class Profile_gpaUpdateView(UpdateView):
    model = Profile_gpa
    form_class = Profile_gpaCreateForm
    context_object_name = 'target_profile_gpa'
    template_name = 'profile_gpaapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})



