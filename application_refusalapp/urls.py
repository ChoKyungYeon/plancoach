from django.urls import path

from application_refusalapp.views import Application_refusalCreateView

app_name = 'application_refusalapp'

urlpatterns = [
    path('create/<int:pk>', Application_refusalCreateView.as_view(), name='create'),
]