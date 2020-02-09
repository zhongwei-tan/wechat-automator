from celery.task import task
from google_sheet import get_authorized_google_client, get_and_save_updated_duty_list
from wechat import wechat_login, send_message_to_chatroom
from utils import duty_string


@task
def duty_reminder(**kwargs):
    reminder_day    = kwargs["reminder_day"].lower()
    service_day     = kwargs["service_day"].lower()
    sheet_name      = kwargs["sheet_name"]
    chatroom        = kwargs["chatroom"]
    template        = kwargs["template"]

    client = get_authorized_google_client()
    duty_info = get_and_save_updated_duty_list(reminder_day, service_day, sheet_name, client)

    if duty_info["updated"]:
        message = template.format(duty_string(duty_info["duty"]))
        send_message_to_chatroom(message, chatroom)

@task
def login_refresh():
    wechat_login()