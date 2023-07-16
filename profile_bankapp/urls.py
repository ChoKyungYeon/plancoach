from django.urls import path

from profile_bankapp.views import Profile_bankUpdateView

app_name = 'profile_bankapp'

urlpatterns = [
    path('update/<int:pk>',Profile_bankUpdateView.as_view(), name='update'),
]