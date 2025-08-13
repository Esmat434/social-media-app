from celery import shared_task
from .email import send_verification_mail_async

@shared_task
def send_verification_mail(to,subject,username,link):
    send_verification_mail_async(to,subject,username,link)