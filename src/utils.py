import datetime
from catalog import datetime_day_number


def check_today(day_of_week: str):
    today = datetime.datetime.today().weekday()
    try:
        if today == datetime_day_number[day_of_week.lower()]:
            return True
        else:
            return False
    except KeyError:
        print(f"'{day_of_week}' is not a day of week!")
        return False

def sense_difference(old: dict, new: dict):
    updated = False
    if old:
        for (old_key, old_value), (new_key, new_value) in zip(old.items(), new.items()):
            if old_value != new_value:
                new[new_key] = new[new_key] + "*"
                updated = True
        return new, updated
    else:
        updated = True
        return new, updated

def duty_string(duty: dict):
    output = ""
    for key, value in duty.items():
        if value == "" or value in "无 " or key in ["日期", "爱宴主厨", "爱宴打扫"]:
            pass
        else:
            output = output + f"{key}: {value}\n"
    return output

def get_service_date(service_day: str):
    service_date = datetime.date.today()
    while service_date.weekday() != datetime_day_number[service_day.lower()]:
        service_date += datetime.timedelta(1)
    return service_date
