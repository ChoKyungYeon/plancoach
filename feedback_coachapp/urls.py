from django.urls import path
from feedback_coachapp.views import Feedback_coachUpdateView, Feedback_coachCreateView, Feedback_coachDeleteView

app_name = 'feedback_coachapp'

urlpatterns = [
    path('create/<int:pk>', Feedback_coachCreateView.as_view(), name='create'),
    path('update/<int:pk>', Feedback_coachUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', Feedback_coachDeleteView.as_view(), name='delete'),
]
