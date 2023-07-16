
from django.urls import path

from teacherapp.views import TeacherDashboardView, TeacherSalaryListView, TeacherApplicationListView

app_name = 'teacherapp'

urlpatterns = [
    path('dashboard/<int:pk>', TeacherDashboardView.as_view(), name='dashboard'),
    path('salarylist/<int:pk>', TeacherSalaryListView.as_view(), name='salarylist'),
    path('applicationlist/<int:pk>', TeacherApplicationListView.as_view(), name='applicationlist'),
]
