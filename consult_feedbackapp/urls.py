from django.urls import path

from consult_feedbackapp.views import Consult_feedbackCreateView, Consult_feedbackListView, \
    Consult_feedbackDeleteView, Consult_feedbackCoachDetailView, Consult_feedbackPlanDetailView, \
    Consult_feedbackUpdateView, Consult_feedbackUpdateContentView

app_name = 'consult_feedbackapp'

urlpatterns = [
    path('create/<int:pk>', Consult_feedbackCreateView.as_view(), name='create'),
    path('list/<int:pk>', Consult_feedbackListView.as_view(), name='list'),
    path('delete/<int:pk>', Consult_feedbackDeleteView.as_view(), name='delete'),
    path('update/<int:pk>', Consult_feedbackUpdateView.as_view(), name='update'),
    path('updatecontent/<int:pk>', Consult_feedbackUpdateContentView.as_view(), name='updatecontent'),
    path('plandetail/<int:pk>', Consult_feedbackPlanDetailView.as_view(), name='plandetail'),
    path('coachdetail/<int:pk>', Consult_feedbackCoachDetailView.as_view(), name='coachdetail')
]