import datetime
from catalog import day_number


def today_is(day_of_week: str):
    today = datetime.datetime.today().weekday()
    try:
        if today == day_number[day_of_week.lower()]:
            return True
        else:
            return False
    except KeyError:
        print("'{}' is not a day of week!".format(day_of_week))
        return False

def sense_difference(old: dict, new: dict):
    updated = False
    for (old_key, old_value), (new_key, new_value) in  zip(old.items(), new.items()):
        if old_value != new_value:
            new[new_key] = new[new_key] + "*"
            updated = True
    return new, updated

def duty_string(duty: dict):
    output = ""
    for key, value in duty.items():
        if value == "" or value in "无 " or key in ["日期", "爱宴主厨", "爱宴打扫", "中心打扫"]:
            pass
        else:
            output = output + "{}: {}\n".format(key, value)
    return output