from datetime import timedelta, date, datetime
from refusalapp.models import Refusal


def time_before(time):
    delta = datetime.now() - time
    if delta.total_seconds() < 300:
        return '방금전'
    elif delta.total_seconds() < 3600:
        minutes = round(delta.total_seconds() / 60)
        return f'{minutes}분 전'
    elif delta.total_seconds() < 86400:
        hours = round(delta.total_seconds() / 3600)
        return f'{hours}시간 전'
    elif delta.total_seconds() < 2592000:
        days = round(delta.total_seconds() / 86400)
        return f'{days}일 전'
    else:
        months = round(delta.total_seconds() / 2592000)
        return f'{months}달 전'


def time_expire(time, expire_duration):
    interval_hours = expire_duration - round((datetime.now() - time) / timedelta(hours=1))
    if interval_hours <= 0:
        return '1시간'
    days, hours = divmod(interval_hours, 24)
    if days > 0:
        interval = f'{days}일'
        if hours > 0:
            interval += f' {hours}시간'
    else:
        interval = f'{hours}시간'
    return interval


def update_field_choices(value, instances, self):
    existing_values = instances.values_list(value, flat=True)
    choices = [
        choice for choice in self.fields[value].choices
        if choice[0] not in existing_values
    ]
    self.fields[value].choices = choices


def profile_completeness_calculator(user):
    target_profile = user.profile
    profile_instance = {
        '학력': hasattr(target_profile, 'profile_scholarship'),
        '고교 성적': hasattr(target_profile, 'profile_gpa'),
        '수능 성적': target_profile.profile_sat.exists(),
        '경력': target_profile.profile_career.exists(),
        '교과목': target_profile.profile_subject.exists(),
        '담당 수업': hasattr(target_profile, 'profile_consulttype'),
        '사진': hasattr(target_profile, 'profile_profileimage'),
        '자기 소개': hasattr(target_profile, 'profile_introduction'),
    }
    profile_completed = [key for key, value in profile_instance.items() if value]
    profile_uncompleted = [key for key, value in profile_instance.items() if not value]
    ratio = round(len(profile_completed) * 100 / len(profile_instance)) if profile_instance else 0
    return profile_completed, profile_uncompleted, ratio


def salaryday_calculator(target_date):
    month_diff = (target_date.day > 10)
    target_month=target_date.month - 1 + month_diff
    new_month = target_month % 12 + 1
    new_year = target_date.year + (target_month // 12)
    if new_month == 12 and target_date.month != 12:
        new_year += 1
    return date(new_year, new_month, 10)

def create_refusal(object, message,type):
    Refusal.objects.create(student=object.student, content=message,type=type)
    object.delete()

