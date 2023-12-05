from django.urls import path

from consult_qnaapp.views import Consult_qnaCreateView, Consult_qnaListView,Consult_qnaUpdateView, Consult_qnaDetailView

app_name = 'consult_qnaapp'

urlpatterns = [
    path('create/<int:pk>', Consult_qnaCreateView.as_view(), name='create'),
    path('list/<int:pk>', Consult_qnaListView.as_view(), name='list'),
    path('update/<int:pk>', Consult_qnaUpdateView.as_view(), name='update'),
    path('detail/<int:pk>', Consult_qnaDetailView.as_view(), name='detail'),
]