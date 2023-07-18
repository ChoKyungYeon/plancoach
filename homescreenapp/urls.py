from django.urls import path

from homescreenapp.views import HomescreenView, ContactView, AboutusView, TermofuseView, PrivacypolicyView, RefundView

app_name = 'homescreenapp'

urlpatterns = [
    path('homescreen/', HomescreenView.as_view(), name='homescreen'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('aboutus/', AboutusView.as_view(), name='aboutus'),
    path('termofuse/', TermofuseView.as_view(), name='termofuse'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('privacypolicy/', PrivacypolicyView.as_view(), name='privacypolicy')
]
