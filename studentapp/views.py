from django.views.generic import DetailView
from accountapp.models import CustomUser

class StudentDashboardView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_step'] = self.object.student_step()
        return context

class StudentRefundListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/refundlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['refunds'] = self.object.refund.all()
        return context