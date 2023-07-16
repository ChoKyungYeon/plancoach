from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from accountapp.models import CustomUser
from profile_bankapp.forms import Profile_bankCreateForm
from profile_bankapp.models import Profile_bank


# 1 비로그인조건 X 2 선생조건 x 3 3학생조건 X 4슈퍼유저 조건 o 5pk 조건 x
class Profile_bankUpdateView(UpdateView):
    model = Profile_bank
    form_class = Profile_bankCreateForm
    context_object_name = 'target_profile_bank'
    template_name = 'profile_bankapp/update.html'
    def get_success_url(self):
        return reverse_lazy('teacherapp:dashboard', kwargs={'pk': self.object.customuser.pk})


