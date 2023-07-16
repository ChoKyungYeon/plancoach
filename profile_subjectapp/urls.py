from django.urls import path

from profile_subjectapp.views import Profile_subjectCreateView, Profile_subjectUpdateView, Profile_subjectDeleteView

app_name = 'profile_subjectapp'

urlpatterns = [
    path('create/<int:pk>', Profile_subjectCreateView.as_view(), name='create'),
    path('update/<int:pk>',Profile_subjectUpdateView.as_view(), name='update'),
    path('delete/<int:pk>',Profile_subjectDeleteView.as_view(), name='delete'),
]