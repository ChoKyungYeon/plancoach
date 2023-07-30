from django.urls import path

from paymentapp.views import PaymentCreateView, PaymentPayView, PaymentCheckView, PaymentResultView, PaymentContactView, \
    PaymentGuideView

from django.urls import path

app_name = 'paymentapp'

urlpatterns = [
    path('create/<int:pk>',PaymentCreateView.as_view(), name='create'),
    path('pay/<int:pk>',PaymentPayView.as_view(), name='pay'),
    path('check/<int:pk>',PaymentCheckView.as_view(), name='check'),
    path('result/<int:pk>',PaymentResultView.as_view(), name='result'),
    path('contact/<int:pk>', PaymentContactView.as_view(), name='contact'),
    path('guide/<int:pk>', PaymentGuideView.as_view(), name='guide'),
]
