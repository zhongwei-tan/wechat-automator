from celery.task import task
from google_sheet import get_authorized_google_client, get_and_save_updated_duty_list
from wechat import wechat_login, send_message_to_chatroom
from utils import duty_string
import yaml


@task
def duty_reminder(reminder_name):
    with open("reminder_list.yml", "r") as file:
        reminders = yaml.load(file, Loader=yaml.FullLoader)
        reminder = reminders[reminder_name]

    reminder_day    = reminder["reminder_day"].lower()
    service_day     = reminder["service_day"].lower()
    sheet_name      = reminder["sheet_name"]
    chatroom        = reminder["chatroom"]
    template        = reminder["template"]

    client = get_authorized_google_client()
    duty_info = get_and_save_updated_duty_list(reminder_day, service_day, sheet_name, client)

    if duty_info["updated"]:
        message = template.format(duty_string(duty_info["duty"]))
        send_message_to_chatroom(message, chatroom)

@task
def login_refresh():
    wechat_login()