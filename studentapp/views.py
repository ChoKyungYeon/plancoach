
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from accountapp.models import CustomUser
from accountapp.utils import user_step_calculator
from plancoach.updaters import request_user_updater


# Create your views here.
@method_decorator(request_user_updater, 'get')
class StudentDashboardView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.object
        target_step, target_consult_pk =user_step_calculator(target_user)
        context['target_consult_pk'] = target_consult_pk
        context['target_step'] = target_step
        return context


class StudentRefundListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/refundlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['refunds'] = self.object.refund.all()
        return context