from datetime import timedelta
from celery.schedules import crontab

CELERY_IMPORTS = ("tasks",)
CELERY_IGNORE_RESULT = False
BROKER_URL = "amqp://rabbitmq:5672"
CELERY_TIMEZONE = "Europe/Berlin"

CELERYBEAT_SCHEDULE = {

    "login_refresh": {
        "task": "tasks.login_refresh",
        "schedule": timedelta(minutes=30),
    },

    "prayer_reminder": {
        "task": "tasks.duty_reminder",
        "schedule": crontab(day_of_week="1-3", hour=8, minute=0),
        "args": ("prayer_reminder",)
    },

    "sunday_service_reminder": {
        "task": "tasks.duty_reminder",
        "schedule": crontab(day_of_week="4-0", hour=8, minute=0),
        "args": ("sunday_service_reminder",)
    },

    "livinghope_service_reminder": {
        "task": "tasks.duty_reminder",
        "schedule": crontab(day_of_week="2-0", hour=8, minute=0),
        "args": ("livinghope_service_reminder",)
    },

    "awake_service_reminder": {
        "task": "tasks.duty_reminder",
        "schedule": crontab(day_of_week="2-0", hour=8, minute=0),
        "args": ("awake_service_reminder",)
    }

}
