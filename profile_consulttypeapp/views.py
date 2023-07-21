from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from profile_consulttypeapp.forms import Profile_consulttypeCreateForm
from profile_consulttypeapp.models import Profile_consulttype
from plancoach.updaters import *
from django.utils.decorators import method_decorator



class Profile_consulttypeUpdateView(UpdateView):
    model = Profile_consulttype
    context_object_name = 'target_profile_consulttype'
    form_class = Profile_consulttypeCreateForm
    template_name = 'profile_consulttypeapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})


class Profile_consulttypeDeleteView(DeleteView):
    model =Profile_consulttype
    context_object_name = 'target_profile_consulttype'
    template_name = 'profile_consulttypeapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})
