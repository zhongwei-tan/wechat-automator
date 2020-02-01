import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dateparser
import datetime
import re
import json
from utils import today_is, sense_difference
from catalog import day_number, reminder_menu


def get_authorized_google_client():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_api_creds.json", scope)
    client = gspread.authorize(creds)
    return client

def get_service_date(service_day: str):
    service_date = datetime.date.today()
    while service_date.weekday() != day_number[service_day.lower()]:
        service_date += datetime.timedelta(1)
    return service_date

def get_duty(sheet_name: str, service_day: str, client: gspread.client.Client):
    duty = None
    sheet = client.open("服事表").worksheet(sheet_name)
    data = sheet.get_all_records()
    service_date = get_service_date(service_day)

    for i, row in enumerate(data):
        row['日期'] = re.sub(r"[.-]", r"/", row['日期'])
        date = dateparser.parse(row['日期'], date_formats=['%d/%m/%Y'])
        if date.day == service_date.day and \
                date.month == service_date.month and \
                date.year == service_date.year:
            duty = row
            break
    return duty

def get_and_save_updated_duty_list(service_day: str, reminder_start_day: str, client: gspread.client.Client):

    service_day = service_day.lower()
    reminder_start_day = reminder_start_day.lower()
    result = {}
    updated = False

    for reminder_category, reminder_dict_list in reminder_menu[service_day].items():
        duty = None
        selected_json_path = None
        selected_sheet_name = None
        # Get duty from latest google sheet data
        for reminder_dict in reminder_dict_list:
            for sheet_name, path in reminder_dict.items():
                duty_buffer = get_duty(sheet_name, service_day, client)
                if duty_buffer:
                    selected_sheet_name = sheet_name
                    selected_json_path = path
                duty = duty or duty_buffer

        if not os.path.exists("saved_json"):
            os.mkdir("saved_json")

        if not os.path.exists(selected_json_path):
            open(selected_json_path, "a").close()

        if today_is(reminder_start_day):
            updated = True
        else:
            try:
                with open(selected_json_path, "r") as f:
                    old_duty = json.load(f)
                duty, updated = sense_difference(old_duty, duty)
            except json.JSONDecodeError:
                pass

        with open(selected_json_path, "w") as f:
            json.dump(duty, f)

        result[selected_sheet_name.lower()] = {"duty": duty, "updated": updated}
    return result  ## dict of dict
