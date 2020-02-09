from datetime import timedelta
import yaml
from utils import add_crontab

CELERY_IMPORTS = ("tasks",)
CELERY_IGNORE_RESULT = False
BROKER_URL = "amqp://rabbitmq:5672"
CELERY_TIMEZONE = "Europe/Berlin"
CELERYBEAT_SCHEDULE = {
    "login_refresh": {
        "task": "tasks.login_refresh",
        "schedule": timedelta(minutes=30),
    },
}

## Open reminder_list.yml and add on reminder tasks
reminder_dict = yaml.load(open("reminder_list.yml"), Loader=yaml.FullLoader)
add_crontab(reminder_dict)
for reminder_name, reminder in reminder_dict.items():
    CELERYBEAT_SCHEDULE[reminder_name] = {
        "task": "tasks.duty_reminder",
        "schedule": reminder["crontab"],
        "kwargs": reminder
    }
