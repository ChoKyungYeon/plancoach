from django.urls import path

from qna_commentapp.views import Qna_commentCreateView, Qna_commentUpdateView

app_name = 'qna_commentapp'

urlpatterns = [
    path('create/<int:pk>', Qna_commentCreateView.as_view(), name='create'),
    path('update/<int:pk>', Qna_commentUpdateView.as_view(), name='update'),
]