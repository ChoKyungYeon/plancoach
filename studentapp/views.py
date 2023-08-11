from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView
from accountapp.models import CustomUser
from django.utils.decorators import method_decorator

from paymentapp.models import Payment
from refundapp.models import Refund
from studentapp.decorators import *

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(StudentDashboardDecorator, name='dispatch')
class StudentDashboardView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/dashboard.html'

    def get(self, request, *args, **kwargs):
        target_user = self.get_object()
        consult_student = getattr(target_user, 'consult_student', None)
        if consult_student:
            if consult_student.state != 'new':
                return redirect('consultapp:dashboard', pk=consult_student.pk)
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_step'] = self.object.student_step()
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(StudentRefundListDecorator, name='dispatch')
class StudentRefundListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'studentapp/refundlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['refunds'] = Refund.objects.filter(student=self.object)
        return context

