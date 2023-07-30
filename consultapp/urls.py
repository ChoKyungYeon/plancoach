from django.urls import path
from consultapp.views import ConsultDashboardView, ConsultCreateView, ConsultInfoUpdateView, ConsultPaymentListView, \
    ConsultApplyDetailView, ConsultExpireView

app_name = 'consultapp'

urlpatterns = [
    path('create/<int:pk>', ConsultCreateView.as_view(), name='create'),
    path('dashboard/<int:pk>', ConsultDashboardView.as_view(), name='dashboard'),
    path('infoupdate/<int:pk>', ConsultInfoUpdateView.as_view(), name='infoupdate'),
    path('paymentlist/<int:pk>', ConsultPaymentListView.as_view(), name='paymentlist'),
    path('applydetail/<int:pk>', ConsultApplyDetailView.as_view(), name='applydetail'),
    path('expire/', ConsultExpireView.as_view(), name='expire'),
]
