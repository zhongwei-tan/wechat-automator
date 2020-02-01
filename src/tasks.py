from celery.task import task
from google_sheet import get_authorized_google_client, get_duty, get_and_save_updated_duty_list
from wechat import wechat_login, send_message_to_chatroom
from utils import duty_string


sunday_template = """大家好,
请注意你在这周末主日崇拜中有服侍任务：
{服事表}
也许你发现服侍的日期有调动，这是有原因的，请体谅，也请按新的服侍表当值。若有困难，请联系蔡师母。

Thanks,
蔡师母
"""

@task
def sunday_service_reminder():

    client = get_authorized_google_client()
    duty_list = get_and_save_updated_duty_list("Sunday", "Thursday", client)

    message = sunday_template.format(服事表=duty_string(duty_list["sunday"]["duty"]))
    if duty_list["sunday"]["updated"]:
        send_message_to_chatroom(message, "Dresden华人基督徒团契")


@task
def wednesday_prayer_meeting_reminder():
    
    client = get_authorized_google_client()
    duty_list = get_and_save_updated_duty_list("Wednesday", "Monday", client)

    message = "周三祷告会负责人：{}".format(duty_list["wednesday"]["duty"]["负责人"])
    if duty_list["wednesday"]["updated"]:
        send_message_to_chatroom(message, "Dresden华人基督徒团契")


@task
def login_refresh():
    wechat_login()