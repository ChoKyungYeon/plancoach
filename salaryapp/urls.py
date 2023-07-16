from django.urls import path

from salaryapp.views import SalaryDetailView, SalaryStateUpdateView, SalaryPayView

app_name = 'salaryapp'

urlpatterns = [
    path('detail/<int:pk>', SalaryDetailView.as_view(), name='detail'),
    path('stateupdate/', SalaryStateUpdateView.as_view(), name='stateupdate'),
    path('pay/<int:pk>', SalaryPayView.as_view(), name='pay'),
]
