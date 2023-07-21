from django.urls import path

from teacherapplyapp.views import TeacherapplyGuideView, TeacherapplyDeleteView, \
    TeacherapplyDetailView, TeacherapplyBankCreateView, TeacherapplyInfoCreateView, TeacherapplyUserimageCreateView, \
    TeacherapplySchoolimageCreateView, TeacherapplyRegisterView

app_name = 'teacherapplyapp'

urlpatterns = [
    path('infocreate/<int:pk>', TeacherapplyInfoCreateView.as_view(), name='infocreate'),
    path('bankcreate/<int:pk>', TeacherapplyBankCreateView.as_view(), name='bankcreate'),
    path('userimagecreate/<int:pk>', TeacherapplyUserimageCreateView.as_view(), name='userimagecreate'),
    path('schoolimagecreate/<int:pk>', TeacherapplySchoolimageCreateView.as_view(), name='schoolimagecreate'),
    path('guide/<int:pk>', TeacherapplyGuideView.as_view(), name='guide'),
    path('delete/<int:pk>', TeacherapplyDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', TeacherapplyDetailView.as_view(), name='detail'),
    path('register/<int:pk>', TeacherapplyRegisterView.as_view(), name='register'),
]