from django.urls import path

from profile_careerapp.views import Profile_careerCreateView, Profile_careerDeleteView, Profile_careerUpdateView

app_name = 'profile_careerapp'

urlpatterns = [
    path('create/<int:pk>', Profile_careerCreateView.as_view(), name='create'),
    path('delete/<int:pk>',Profile_careerDeleteView.as_view(), name='delete'),
    path('update/<int:pk>',Profile_careerUpdateView.as_view(), name='update'),
]