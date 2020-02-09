import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dateparser
import datetime
import re
import json
from utils import today_is, sense_difference
from catalog import datetime_day_number


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
    while service_date.weekday() != datetime_day_number[service_day.lower()]:
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

def get_and_save_updated_duty_list(reminder_start_day: str, 
                                   service_day: str, 
                                   sheet_name: str,
                                   client: gspread.client.Client):

    reminder_start_day = reminder_start_day
    service_day = service_day
    updated = False
    path = "saved_json/{}.json".format(sheet_name.lower().replace(" ", "_"))

    if not os.path.exists("saved_json"):
        os.mkdir("saved_json")
    if not os.path.exists(path):
        open(path, "a").close()
        
    duty = get_duty(sheet_name, service_day, client)

    if today_is(reminder_start_day):
        updated = True
    else:
        try:
            with open(path, "r") as f:
                old_duty = json.load(f)
            duty, updated = sense_difference(old_duty, duty)
        except json.JSONDecodeError:
            pass

    with open(path, "w") as f:
        json.dump(duty, f)
    return {"duty": duty, "updated": updated}