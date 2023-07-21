from django.shortcuts import redirect
from django.views.generic import DetailView
from accountapp.models import CustomUser
from plancoach.updaters import *
from django.utils.decorators import method_decorator

class StudentDashboardView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/dashboard.html'

    def get(self, request, *args, **kwargs):
        target_user = self.get_object()
        if hasattr(target_user, 'consult_student'):
            return redirect('consultapp:dashboard', pk=target_user.consult_student.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_step'] = self.object.step()
        return context

class StudentRefundListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/refundlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['refunds'] = self.object.refund.all()
        return context