
from django.urls import path

from superuserapp.views import SuperuserDashboardView

app_name = 'superuserapp'

urlpatterns = [
    path('dashboard/', SuperuserDashboardView.as_view(), name='dashboard'),
]
