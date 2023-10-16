from django.urls import path

from reviewapp.views import ReviewCreateView, ReviewManageView, ReviewListView, ReviewDeleteView

app_name = 'reviewapp'

urlpatterns = [
    path('create', ReviewCreateView.as_view(), name='create'),
    path('manage',ReviewManageView.as_view(), name='manage'),
    path('list', ReviewListView.as_view(), name='list'),
    path('delete/<int:pk>', ReviewDeleteView.as_view(), name='delete'),
]