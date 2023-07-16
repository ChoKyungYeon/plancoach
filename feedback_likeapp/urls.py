from django.urls import path

from feedback_likeapp.views import Feedback_likeView

app_name = 'feedback_likeapp'

urlpatterns = [
    path('like/',Feedback_likeView.as_view(), name='like'),
]