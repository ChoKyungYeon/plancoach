from django.urls import path

from qna_likeapp.views import Qna_likeView

app_name = 'qna_likeapp'

urlpatterns = [
    path('like/',Qna_likeView.as_view(), name='like'),
]