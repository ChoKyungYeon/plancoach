from django.urls import path
from feedback_planapp.views import Feedback_planUpdateView, Feedback_planStateUpdateView

app_name = 'feedback_planapp'

urlpatterns = [
    path('update/<int:pk>', Feedback_planUpdateView.as_view(), name='update'),
    path('stateupdate/', Feedback_planStateUpdateView.as_view(), name='stateupdate'),
]
