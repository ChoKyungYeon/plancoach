from django.urls import path

from refusalapp.views import RefusalCreateView

app_name = 'refusalapp'

urlpatterns = [
    path('create/<int:pk>', RefusalCreateView.as_view(), name='create'),
]