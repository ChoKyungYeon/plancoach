from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView

from consult_classlinkapp.decorators import *
from consult_classlinkapp.forms import Consult_classlinkCreateForm
from consult_classlinkapp.models import Consult_classlink
from django.utils.decorators import method_decorator

from consultapp.models import Consult


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_classlinkCreateDecorator, name='dispatch')
class Consult_classlinkCreateView(CreateView):
    model = Consult_classlink
    form_class = Consult_classlinkCreateForm
    template_name = 'consult_classlinkapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        context['target_consult'] = consult
        return context

    def form_valid(self, form):
        consult = get_object_or_404(Consult, pk=self.kwargs['pk'])
        with transaction.atomic():
            form.instance.consult = consult
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('consultapp:dashboard', kwargs={'pk': self.kwargs['pk']})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Consult_classlinkUpdateDecorator, name='dispatch')
class Consult_classlinkUpdateView(UpdateView):
    model = Consult_classlink
    form_class = Consult_classlinkCreateForm
    context_object_name = 'target_consult_classlink'
    template_name = 'consult_classlinkapp/update.html'

    def get_success_url(self):
        return reverse_lazy('consultapp:dashboard', kwargs={'pk': self.object.consult.pk})
