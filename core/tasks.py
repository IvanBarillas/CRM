# core/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_task():
    subject = "Congratulations"
    message = "Se ha configurado Celery correctamente."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['mario@barillas.io']
    
    send_mail(subject, message, from_email, recipient_list)
    return "Email sent!"
