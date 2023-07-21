from django.shortcuts import get_object_or_404
from accountapp.models import CustomUser
from applicationapp.models import Application
from consult_feedbackapp.models import Consult_feedback
from consultapp.models import Consult
from feedback_coachapp.models import Feedback_coach
from feedback_planapp.models import Feedback_plan
from phonenumberapp.models import Phonenumber
from qna_commentapp.models import Qna_comment


def application_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Application, pk=kwargs['pk']).updater()
        return func(request, *args, **kwargs)
    return decorated

def consult_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Consult, pk=kwargs['pk']).updater()
        return func(request, *args, **kwargs)
    return decorated

def user_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(CustomUser, pk=kwargs['pk']).updater()
        return func(request, *args, **kwargs)
    return decorated

def request_user_updater(func):
    def decorated(request, *args, **kwargs):
        request.user.updater()
        return func(request, *args, **kwargs)
    return decorated

def feedback_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Consult_feedback, pk=kwargs['pk']).consult.updater()
        return func(request, *args, **kwargs)
    return decorated

def qna_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Consult_feedback, pk=kwargs['pk']).consult.updater()
        return func(request, *args, **kwargs)
    return decorated

def comment_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Qna_comment, pk=kwargs['pk']).consult_qna.consult.updater()
        return func(request, *args, **kwargs)
    return decorated


def plan_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Feedback_plan, pk=kwargs['pk']).consult_feedback.consult.updater()
        return func(request, *args, **kwargs)
    return decorated


def coach_updater(func):
    def decorated(request, *args, **kwargs):
        get_object_or_404(Feedback_coach, pk=kwargs['pk']).consult_feedback.consult.updater()
        return func(request, *args, **kwargs)
    return decorated


def phonenumber_updater(func):
    def decorated(request, *args, **kwargs):
        for phonenumber in Phonenumber.objects.all():
            phonenumber.updater()
        return func(request, *args, **kwargs)
    return decorated
