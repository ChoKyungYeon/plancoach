from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView
from profile_bankapp.forms import Profile_bankManageForm
from profile_bankapp.models import Profile_bank
from django.utils.decorators import method_decorator

from profileapp.decorators import Profile_instanceManageDecorator

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Profile_instanceManageDecorator, name='dispatch')
class Profile_bankManageView(UpdateView):
    model = Profile_bank
    form_class = Profile_bankManageForm
    context_object_name = 'target_profile_bank'
    template_name = 'profile_bankapp/manage.html'
    def get_success_url(self):
        return reverse_lazy('teacherapp:dashboard', kwargs={'pk': self.object.profile.teacher.pk})


