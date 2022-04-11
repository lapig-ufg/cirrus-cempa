from cirrus.util.config import settings
from cirrus.util.config import logger
import notifiers

params = {
    "username": settings.EMAIL_ADDRESS,
    "password": settings.EMAIL_PASSWORD,
    "subject": f"[logger] {settings.EMAIL_SUBJECT}",
    "to":  settings.EMAIL_LIST,
    'from' :settings.EMAIL_ADDRESS,
    'host': settings.EMAIL_HOST, 
    'port':settings.EMAIL_PORT,
    'tls': False, 'ssl': False, 'html': False

}
print(params)
# Send a single notification
notifier = notifiers.get_notifier("email")
notifier.notify(message="The application is running!", **params)

# Be alerted on each error message
from notifiers.logging import NotificationHandler

handler = NotificationHandler("email", defaults=params)
logger.add(handler, level="ERROR")

logger.error('teste')
