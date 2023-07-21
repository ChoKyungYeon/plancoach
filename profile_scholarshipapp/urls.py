from django.urls import path

from profile_scholarshipapp.views import Profile_scholarshipUpdateView, Profile_scholarshipManageView

app_name = 'profile_scholarshipapp'

urlpatterns = [
    path('update/<int:pk>',Profile_scholarshipUpdateView.as_view(), name='update'),
    path('manage/<int:pk>',Profile_scholarshipManageView.as_view(), name='manage'),
]