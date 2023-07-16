from django.urls import path

from profile_consulttypeapp.views import Profile_consulttypeUpdateView, Profile_consulttypeDeleteView

app_name = 'profile_consulttypeapp'

urlpatterns = [
    path('update/<int:pk>',Profile_consulttypeUpdateView.as_view(), name='update'),
    path('delete/<int:pk>',Profile_consulttypeDeleteView.as_view(), name='delete'),
]