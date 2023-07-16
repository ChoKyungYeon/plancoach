from django.urls import path

from profileapp.views import ProfileTuitionUpdateView, ProfileDetailView, ProfileStateUpdateView, \
    ProfileListView, ProfileCreateView, ProfileDeleteView

app_name = 'profileapp'

urlpatterns = [
    path('tuitionupdate/<int:pk>',ProfileTuitionUpdateView.as_view(), name='tuitionupdate'),
    path('create/<int:pk>',ProfileCreateView.as_view(), name='create'),
    path('stateupdate/',ProfileStateUpdateView.as_view(), name='stateupdate'),
    path('detail/<int:pk>',ProfileDetailView.as_view(), name='detail'),
    path('delete/<int:pk>',ProfileDeleteView.as_view(), name='delete'),
    path('list', ProfileListView.as_view(), name='list'),
]