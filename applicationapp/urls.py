from django.urls import path

from applicationapp.views import ApplicationCreateView, ApplicationDeleteView, ApplicationUpdateView, \
    ApplicationDetailView, ApplicationStateUpdateView, ApplicationResultView, ApplicationGuideView

app_name = 'applicationapp'

urlpatterns = [
    path('create/<int:pk>', ApplicationCreateView.as_view(), name='create'),
    path('delete/<int:pk>',ApplicationDeleteView.as_view(), name='delete'),
    path('update/<int:pk>',ApplicationUpdateView.as_view(), name='update'),
    path('detail/<int:pk>',ApplicationDetailView.as_view(), name='detail'),
    path('stateupdate',ApplicationStateUpdateView.as_view(), name='stateupdate'),
    path('guide/<int:pk>',ApplicationGuideView.as_view(), name='guide'),
    path('result',ApplicationResultView.as_view(), name='result'),
]