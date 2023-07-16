from django.urls import path

from profile_profileimageapp.views import Profile_profileimageCreateView, \
    Profile_profileimageDeleteView

app_name = 'profile_profileimageapp'

urlpatterns = [
    path('create/<int:pk>', Profile_profileimageCreateView.as_view(), name='create'),
    path('delete/<int:pk>',Profile_profileimageDeleteView.as_view(), name='delete'),
]