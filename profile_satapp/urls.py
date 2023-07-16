from django.urls import path

from profile_satapp.views import Profile_satCreateView, Profile_satDeleteView, Profile_satUpdateView

app_name = 'profile_satapp'

urlpatterns = [
    path('create/<int:pk>', Profile_satCreateView.as_view(), name='create'),
    path('delete/<int:pk>',Profile_satDeleteView.as_view(), name='delete'),
    path('update/<int:pk>',Profile_satUpdateView.as_view(), name='update'),
]