from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from profile_profileimageapp.forms import Profile_profileimageCreateForm
from profile_profileimageapp.models import Profile_profileimage
from profileapp.models import Profile
from plancoach.updaters import *
from django.utils.decorators import method_decorator

class Profile_profileimageCreateView(CreateView):
    model = Profile_profileimage
    form_class = Profile_profileimageCreateForm
    template_name = 'profile_profileimageapp/create.html'

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

class Profile_profileimageDeleteView(DeleteView):
    model = Profile_profileimage
    context_object_name = 'target_profile_profileimage'
    template_name = 'profile_profileimageapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})
