from applicationapp.models import Application
from consultapp.models import Consult
from plancoach.updaters import user_updater
from refundapp.models import Refund


def user_step_calculator(target_user):
    user_updater(target_user)
    if not target_user.is_authenticated:
        return 'unauthenticated', None
    if target_user.state == 'teacher':
        return 'teacher', None
    if target_user.state == 'superuser':
        return 'superuser', None
    application = Application.objects.filter(student=target_user).first()
    state_to_step = {
        'step1': 'step1',
        'denied': 'denied',
        'refund': 'refund',
        'matching': 'step4',
        'applied': 'step3',
        'waiting': 'step5',
        'ongoing': 'ongoing'
    }
    if application:
        state = application.state
    else:

        state = 'refund' if Refund.objects.filter(student=target_user, is_given=False).first() else 'step1'
    step = state_to_step.get(state, 'step3')
    consult_pk = None
    if state in ['waiting', 'ongoing']:
        consult_pk = Consult.objects.get(student=target_user).pk
    return step, consult_pk

def can_apply_teacher(student):
    target_step,consult_pk =user_step_calculator(student)
    return target_step == 'step1' or target_step == 'denied'

def can_user_apply(student):
    target_step,consult_pk=user_step_calculator(student)
    return target_step == 'step1' or target_step == 'denied'