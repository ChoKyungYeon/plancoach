from datetime import datetime,  date



def salaryday_calculator(target_date):
    month_diff = (target_date.day >= 10)
    new_month = (target_date.month - 1 + month_diff) % 12 + 1
    new_year = target_date.year + (target_date.month - 1 + month_diff) // 12
    return date(new_year, new_month, 10)