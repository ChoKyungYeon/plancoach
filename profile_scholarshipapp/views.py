from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView

from plancoach.decorators import is_teacher
from profile_scholarshipapp.decorators import profile_scholarship_ownership_required
from profile_scholarshipapp.forms import Profile_scholarshipCreateForm, Profile_scholarshipManageForm
from profile_scholarshipapp.models import Profile_scholarship





class Profile_scholarshipDeleteView(DeleteView):
    model = Profile_scholarship
    context_object_name = 'target_profile_scholarship'
    template_name = 'profile_scholarshipapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})


class Profile_scholarshipUpdateView(UpdateView):
    model = Profile_scholarship
    form_class = Profile_scholarshipCreateForm
    context_object_name = 'target_profile_scholarship'
    template_name = 'profile_scholarshipapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})

class Profile_scholarshipManageView(UpdateView):
    model = Profile_scholarship
    form_class = Profile_scholarshipManageForm
    context_object_name = 'target_profile_scholarship'
    template_name = 'profile_scholarshipapp/manage.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})

