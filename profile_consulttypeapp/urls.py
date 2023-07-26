from django.urls import path

from profile_consulttypeapp.views import Profile_consulttypeUpdateView

app_name = 'profile_consulttypeapp'

urlpatterns = [
    path('update/<int:pk>',Profile_consulttypeUpdateView.as_view(), name='update'),
]