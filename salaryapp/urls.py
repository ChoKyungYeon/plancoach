from django.urls import path

from salaryapp.views import SalaryExpectedView, SalaryStateUpdateView, SalaryPayView, SalaryDetailView

app_name = 'salaryapp'

urlpatterns = [
    path('detail/<int:pk>', SalaryDetailView.as_view(), name='detail'),
    path('expected/<int:pk>', SalaryExpectedView.as_view(), name='expected'),
    path('stateupdate/', SalaryStateUpdateView.as_view(), name='stateupdate'),
    path('pay/<int:pk>', SalaryPayView.as_view(), name='pay'),
]
