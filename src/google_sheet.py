import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dateparser
import datetime

day_number = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}

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
    while service_date.weekday() != day_number[service_day]:
        service_date += datetime.timedelta(1)
    return service_date

def get_duty(service_day: str, client: gspread.client.Client):
    duty = None
    sheet = client.open("服事表").worksheet(service_day)
    data = sheet.get_all_records()
    service_date = get_service_date(service_day)

    for i, row in enumerate(data):
        date = dateparser.parse(row['日期'], date_formats=['%d/%m/%Y'])
        if date.day == service_date.day and \
                date.month == service_date.month and \
                date.year == service_date.year:
            duty = row
            break
    return duty