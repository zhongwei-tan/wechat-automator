from celery.schedules import crontab
from datetime import timedelta

CELERY_IMPORTS = ('tasks',)
CELERY_IGNORE_RESULT = False
BROKER_URL = 'amqp://rabbitmq:5672'
CELERY_TIMEZONE = 'Europe/Berlin'

CELERYBEAT_SCHEDULE = {

    'login_refresh':{
        'task': 'tasks.login_refresh',
        'schedule': timedelta(minutes=30),
    },

    'sunday_service_reminder': {
        'task': 'tasks.sunday_service_reminder',
        'schedule': crontab(day_of_week='thursday', hour=8, minute=0),
    },

    'wednesday_prayer_meeting_reminder': {
        'task': 'tasks.wednesday_prayer_meeting_reminder',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),
    }

}