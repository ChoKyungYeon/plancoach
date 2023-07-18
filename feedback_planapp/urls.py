from django.urls import path
from feedback_planapp.views import Feedback_planUpdateView

app_name = 'feedback_planapp'

urlpatterns = [
    path('update/<int:pk>', Feedback_planUpdateView.as_view(), name='update'),
]
