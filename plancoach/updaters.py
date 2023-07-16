from datetime import timedelta, datetime

from django.db import transaction

from plancoach.variables import current_date, current_datetime


def consult_updater(target_consult):
    today = current_date
    extenddate = target_consult.extenddate()
    extend_enddate = target_consult.extend_enddate()
    consult_state = target_consult.state
    consult_application = target_consult.application

    if consult_state == 'unextended' and extenddate <= today:
        consult_application.delete()
        target_consult.delete()

    elif consult_state == 'extended':
        if extend_enddate <= today:
            consult_application.delete()
            target_consult.delete()
        elif extenddate <= today < extend_enddate:
            target_consult.startdate = extenddate
            target_consult.state = 'unextended'
            target_consult.save()

def application_updater(target_application):
    application_state=target_application.state
    created_at = target_application.created_at
    updated_at = target_application.updated_at
    created_interval = current_datetime - created_at
    updated_interval = current_datetime - updated_at if updated_at else None
    with transaction.atomic():
        if application_state == 'applied':
            if created_interval > timedelta(hours=48):
                target_application.delete()
            elif timedelta(hours=48) >= created_interval > timedelta(hours=24):
                target_application.state = 'denied'
                target_application.updated_at = created_at + timedelta(hours=24)
                target_application.save()

        elif application_state == 'denied':
            if updated_interval > timedelta(hours=24):
                target_application.delete()

        elif application_state == 'matching':
            if updated_interval > timedelta(hours=168):
                target_application.delete()
        elif application_state == 'waiting':
            consult = target_application.consult
            if not consult.state == 'new':
                target_application.state = 'ongoing'
                target_application.save()
                consult_updater(consult)
            else:
                if updated_interval > timedelta(hours=48):
                    consult.delete()
                    target_application.delete()

        elif application_state == 'ongoing':
            consult_updater(target_application.consult)


def student_updater(student):
    target_application = getattr(student, 'application_student', None)
    if target_application:
        application_updater(target_application)

def teacher_updater(teacher):
    applications =teacher.application_teacher.all()
    if applications:
        for application in applications:
            application_updater(application)


def user_updater(target_user):
    if target_user.is_authenticated:
        user_state=target_user.state
        if user_state == 'teacher':
            teacher_updater(target_user)
        elif user_state == 'student':
            student_updater(target_user)



def request_user_updater(func):
    def decorated(request, *args, **kwargs):
        user_updater(request.user)
        return func(request, *args, **kwargs)
    return decorated

# usestep_calculater

