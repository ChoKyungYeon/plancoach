
from django.urls import path

from superuserapp.views import SuperuserDashboardView, SuperuserPageviewView

app_name = 'superuserapp'

urlpatterns = [
    path('dashboard/', SuperuserDashboardView.as_view(), name='dashboard'),
    path('pageview/', SuperuserPageviewView.as_view(), name='pageview'),
]
