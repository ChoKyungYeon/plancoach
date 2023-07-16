from django.urls import path

from profile_likeapp.views import Profile_likeView

app_name = 'profile_likeapp'

urlpatterns = [
    path('like/',Profile_likeView.as_view(), name='like'),
]