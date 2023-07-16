from django.urls import path

from refundapp.views import RefundCreateView, RefundGuideView, RefundStateUpdateView, RefundDetailView

app_name = 'refundapp'

urlpatterns = [
    path('guide/<int:pk>',RefundGuideView.as_view(), name='guide'),
    path('create/<int:pk>',RefundCreateView.as_view(), name='create'),
    path('detail/<int:pk>',RefundDetailView.as_view(), name='detail'),
    path('create/<int:pk>',RefundCreateView.as_view(), name='create'),
    path('stateupdate', RefundStateUpdateView.as_view(), name='stateupdate'),
]