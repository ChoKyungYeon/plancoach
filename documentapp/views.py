from django.urls import reverse_lazy
from documentapp.forms import DocumentCreateForm
from documentapp.models import Document
from django.views.generic import UpdateView, CreateView


class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = 'documentapp/create.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')

class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentCreateForm
    context_object_name = 'target_document'
    template_name = 'documentapp/update.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:dashboard')


