
from datetime import timedelta

from plancoach.variables import current_datetime


def time_converter_before(time):
    interval_hours = round((current_datetime - time) / timedelta(hours=1))
    if interval_hours >= 24:
        return f'{interval_hours // 24}일 전'
    elif interval_hours == 0:
        return '방금 전'
    return f'{interval_hours}시간 전'

def time_before(time):
    delta = current_datetime - time

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

def time_converter_expire(time, expire_duration):
    interval_hours = expire_duration - round((current_datetime - time) / timedelta(hours=1))
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