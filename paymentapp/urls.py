from django.urls import path

from paymentapp.views import PaymentCreateView, PaymentPayView, PaymentCheckView, PaymentResultView, PaymentContactView

from django.urls import path

app_name = 'paymentapp'

urlpatterns = [
    path('create/<int:pk>',PaymentCreateView, name='create'),
    path('pay/<int:pk>',PaymentPayView, name='pay'),
    path('check/<int:pk>',PaymentCheckView, name='check'),
    path('result/<int:pk>',PaymentResultView, name='result'),
    path('contact/<int:pk>', PaymentContactView.as_view(), name='contact'),
]
