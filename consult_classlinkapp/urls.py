from django.urls import path

from consult_classlinkapp.views import Consult_classlinkCreateView, Consult_classlinkUpdateView

app_name = 'consult_classlinkapp'

urlpatterns = [
    path('create/<int:pk>', Consult_classlinkCreateView.as_view(), name='create'),
    path('update/<int:pk>', Consult_classlinkUpdateView.as_view(), name='update'),
]
