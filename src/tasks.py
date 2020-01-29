from celery.task import task
from google_sheet import get_authorized_google_client, get_duty
from wechat import wechat_login, send_message_to_chatroom


sunday_template = '''大家好,
请注意你在这周末主日崇拜中有服侍任务：
司会：{司会}
诗歌敬拜：{敬拜}
证道：{证道}
圣餐：{圣餐}
音控：{音控}
茶点：{茶点}
接待：{接待}
儿童主日学小班：{小班}
儿童主日学大班：{大班}

也许你发现服侍的日期有调动，这是有原因的，请体谅，也请按新的服侍表当值。若有困难，请联系蔡师母。

Thanks,
蔡师母
'''

@task
def sunday_service_reminder():

    client = get_authorized_google_client()
    duty = get_duty('Sunday', client)
    message = sunday_template.format(
        司会=duty['司会'],
        敬拜=duty['诗歌敬拜'],
        证道=duty['证道'],
        圣餐='-' if (duty['圣餐']=='' or duty['圣餐']=='无') else duty['圣餐'],
        音控=duty['音控'],
        茶点=duty['茶点'],
        接待=duty['接待'],
        小班=duty['小班'],
        大班=duty['大班']
    )
    send_message_to_chatroom(message, 'Dresden华人基督徒团契')


@task
def wednesday_prayer_meeting_reminder():
    
    client = get_authorized_google_client()
    duty = get_duty('Wednesday', client)
    message = '周三祷告会负责人：{}'.format(duty['负责人'])
    send_message_to_chatroom(message, 'Dresden华人基督徒团契')


@task
def login_refresh():
    wechat_login()