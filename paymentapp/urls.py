from django.urls import path

from paymentapp.views import PaymentCreateView, PaymentGuideView, PaymentPayView, PaymentStateUpdateView, \
    PaymentDeleteView
from django.urls import path

app_name = 'paymentapp'

urlpatterns = [
    path('create/<int:pk>',PaymentCreateView.as_view(), name='create'),
    path('guide/<int:pk>', PaymentGuideView.as_view(), name='guide'),
    path('guide/<int:pk>', PaymentGuideView.as_view(), name='guide'),
    path('pay/<int:pk>', PaymentPayView.as_view(), name='pay'),
    path('stateupdate/', PaymentStateUpdateView.as_view(), name='stateupdate'),
    path('delete/<int:pk>', PaymentDeleteView.as_view(), name='delete'),
]

