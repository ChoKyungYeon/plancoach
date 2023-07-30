
from django.urls import path

from studentapp.views import StudentDashboardView,StudentRefundListView

app_name = 'studentapp'

urlpatterns = [
    path('dashboard/<int:pk>', StudentDashboardView.as_view(), name='dashboard'),
    path('refundlist/<int:pk>', StudentRefundListView.as_view(), name='refundlist'),
    path('notfound/<int:pk>', StudentRefundListView.as_view(), name='notfound'),
]
