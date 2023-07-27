"""basicframe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='homescreens/homescreen', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accountapp.urls')),
    path('homescreens/', include('homescreenapp.urls')),

    path('teachers/', include('teacherapp.urls')),
    path('students/', include('studentapp.urls')),
    path('superusers/', include('superuserapp.urls')),

    #프로필
    path('profiles/', include('profileapp.urls')),
    path('profile_careers/', include('profile_careerapp.urls')),
    path('profile_scholarships/', include('profile_scholarshipapp.urls')),
    path('profile_subjects/', include('profile_subjectapp.urls')),
    path('profile_consulttypes/', include('profile_consulttypeapp.urls')),
    path('profile_sats/', include('profile_satapp.urls')),
    path('profile_gpas/', include('profile_gpaapp.urls')),
    path('profile_likes/', include('profile_likeapp.urls')),
    path('profile_introductions/', include('profile_introductionapp.urls')),
    path('profile_profileimages/', include('profile_profileimageapp.urls')),
    path('profile_banks/', include('profile_bankapp.urls')),

    #컨설팅 관련
    path('consults/', include('consultapp.urls')),
    path('consult_classlinks/', include('consult_classlinkapp.urls')),
    path('consult_feedbacks/', include('consult_feedbackapp.urls')),
    path('consult_qnas/', include('consult_qnaapp.urls')),
    path('feedback_plans/', include('feedback_planapp.urls')),
    path('feedback_coachs/', include('feedback_coachapp.urls')),
    path('feedback_likes/', include('feedback_likeapp.urls')),
    path('qna_likes/', include('qna_likeapp.urls')),
    path('qna_comments/', include('qna_commentapp.urls')),

    path('applications/', include('applicationapp.urls')),
    path('refusals/', include('refusalapp.urls')),

    path('payments/', include('paymentapp.urls')),

    path('phonenumbers/', include('phonenumberapp.urls')),
    path('salarys/', include('salaryapp.urls')),
    path('refunds/', include('refundapp.urls')),
    path('teacherapplys/', include('teacherapplyapp.urls')),
    path('documents/', include('documentapp.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

