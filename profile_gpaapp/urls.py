from django.urls import path

from profile_gpaapp.views import Profile_gpaCreateView, Profile_gpaDeleteView, Profile_gpaUpdateView

app_name = 'profile_gpaapp'

urlpatterns = [
    path('create/<int:pk>', Profile_gpaCreateView.as_view(), name='create'),
    path('delete/<int:pk>',Profile_gpaDeleteView.as_view(), name='delete'),
    path('update/<int:pk>',Profile_gpaUpdateView.as_view(), name='update'),
]