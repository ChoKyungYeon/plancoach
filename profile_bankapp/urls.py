from django.urls import path

from profile_bankapp.views import Profile_bankManageView

app_name = 'profile_bankapp'

urlpatterns = [
    path('manage/<int:pk>',Profile_bankManageView.as_view(), name='manage'),
]