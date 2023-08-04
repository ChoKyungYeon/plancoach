from django.contrib.auth.views import LogoutView
from django.urls import path

from accountapp import views
from accountapp.views import AccountDeleteView, AccountCreateView, AccountLoginView, AccountSettingView, \
    AccountInfoUpdateView, AccountPasswordUpdateView, AccountNotificationUpdateView, AccountPasswordResetView, \
    test_student, test_superuser

app_name = 'accountapp'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('infoupdate/<int:pk>', AccountInfoUpdateView.as_view(), name='infoupdate'),
    path('passwordupdate/<int:pk>', AccountPasswordUpdateView.as_view(), name='passwordupdate'),
    path('passwordreset/<int:pk>', AccountPasswordResetView.as_view(), name='passwordreset'),
    path('notificationupdate/', AccountNotificationUpdateView.as_view(), name='notificationupdate'),
    path('delete/<int:pk>', AccountDeleteView.as_view(), name='delete'),
    path('create/<int:pk>', AccountCreateView.as_view(), name='create'),
    path('setting/<int:pk>', AccountSettingView.as_view(), name='setting'),
    path('test_student/', test_student, name='test_student'),
    path('test_superuser/', test_superuser, name='test_superuser'),
    path('test_teacher/', test_superuser, name='test_teacher'),
]
