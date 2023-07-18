from datetime import timedelta


def planatime_calulator(start_date):
    datelist = []
    for i in range(1, 8):
        new_date = start_date + timedelta(days=i)
        datelist.append(new_date)
    return datelist
