from django.urls import path

from refusalapp.views import RefusalApplicationRefuseView, RefusalTeacherapplyRefuseView

app_name = 'refusalapp'

urlpatterns = [
    path('applicationrefuse/<int:pk>', RefusalApplicationRefuseView.as_view(), name='applicationrefuse'),
    path('teacherapplyrefuse/<int:pk>', RefusalTeacherapplyRefuseView.as_view(), name='teacherapplyrefuse'),
]