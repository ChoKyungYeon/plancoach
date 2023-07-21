from django.urls import path

from refundapp.views import RefundCreateView, RefundGuideView, RefundStateUpdateView, RefundDetailView, RefundPayView

app_name = 'refundapp'

urlpatterns = [
    path('guide/<int:pk>',RefundGuideView.as_view(), name='guide'),
    path('create/<int:pk>',RefundCreateView.as_view(), name='create'),
    path('detail/<int:pk>',RefundDetailView.as_view(), name='detail'),
    path('pay/<int:pk>',RefundPayView.as_view(), name='pay'),
    path('create/<int:pk>',RefundCreateView.as_view(), name='create'),
    path('stateupdate', RefundStateUpdateView.as_view(), name='stateupdate'),
]