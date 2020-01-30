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

def sense_difference(old_list: list, new_list: list):
    updated = False
    for i, (dict_1, dict_2) in enumerate(zip(old_list, new_list)):
        for k in dict_1:
            if dict_1[k] != dict_2[k]:
                new_list[i][k] = new_list[i][k] + "*"
                updated = True
    return new_list, updated


def duty_string(duty: dict):
    output = ""
    for key, value in duty.items():
        if value == "" or value in "无 " or key in ["日期", "爱宴主厨", "爱宴打扫", "中心打扫"]:
            pass
        else:
            output = output + "{}: {}\n".format(key, value)
    return output