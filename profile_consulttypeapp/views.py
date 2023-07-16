from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from plancoach.decorators import is_teacher
from profile_consulttypeapp.decorators import profile_consulttype_ownership_required
from profile_consulttypeapp.forms import Profile_consulttypeCreateForm
from profile_consulttypeapp.models import Profile_consulttype




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
