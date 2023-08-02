from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView
from profile_scholarshipapp.decorators import *
from profile_scholarshipapp.forms import Profile_scholarshipUpdateForm, Profile_scholarshipManageForm
from profile_scholarshipapp.models import Profile_scholarship
from django.utils.decorators import method_decorator

from profileapp.decorators import Profile_instanceManageDecorator

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Profile_scholarshipEditDecorator, name='dispatch')
class Profile_scholarshipUpdateView(UpdateView):
    model = Profile_scholarship
    form_class = Profile_scholarshipUpdateForm
    context_object_name = 'target_profile_scholarship'
    template_name = 'profile_scholarshipapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Profile_instanceManageDecorator, name='dispatch')
class Profile_scholarshipManageView(UpdateView):
    model = Profile_scholarship
    form_class = Profile_scholarshipManageForm
    context_object_name = 'target_profile_scholarship'
    template_name = 'profile_scholarshipapp/manage.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})

