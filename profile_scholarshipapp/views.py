from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from profile_scholarshipapp.forms import Profile_scholarshipUpdateForm, Profile_scholarshipManageForm
from profile_scholarshipapp.models import Profile_scholarship
from plancoach.updaters import *
from django.utils.decorators import method_decorator


class Profile_scholarshipUpdateView(UpdateView):
    model = Profile_scholarship
    form_class = Profile_scholarshipUpdateForm
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

