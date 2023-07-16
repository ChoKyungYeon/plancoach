from phonenumberapp.views import PhonenumberSignupCreateView, PhonenumberSignupVerifyView, PhonenumberSearchVerifyView, \
    PhonenumberSearchCreateView, PhonenumberUpdateVerifyView, PhonenumberUpdateCreateView
from django.urls import path


app_name = 'phonenumberapp'

urlpatterns = [
    path('signupverify/<int:pk>',PhonenumberSignupVerifyView.as_view(), name='signupverify'),
    path('signupcreate/',PhonenumberSignupCreateView.as_view(), name='signupcreate'),
    path('searchverify/<int:pk>',PhonenumberSearchVerifyView.as_view(), name='searchverify'),
    path('searchcreate/',PhonenumberSearchCreateView.as_view(), name='searchcreate'),
    path('updateverify/<int:pk>',PhonenumberUpdateVerifyView.as_view(), name='updateverify'),
    path('updatecreate/<int:pk>',PhonenumberUpdateCreateView.as_view(), name='updatecreate'),
]
