# portal/taks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_access_enduser_email(email, token):
    subject = 'Tu enlace de acceso'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]
    
    text_content = (
        f"Hola, {email}!\n\n"
        "Usted ha sido invitado a realizar inicio de sesión en el portal CRM Mesa de Ayuda.\n\n"
        "Click en el link para iniciar sesión en el Portal\n\n"
        f"{settings.SITE_URL}/portal/access/{token}/\n\n"
        "El enlace de invitación anterior es válido solo por un corto período de tiempo, así que inicie sesión rápidamente.\n\n"
        "Gracias por Contactarnos!\n"
        "---------------------------------------------------------------------------------\n"
        "¿Por qué recibió este correo electrónico? ¡Me alegra que hayas preguntado! Estamos usando Workspace IT mesa de ayuda para rastrear problemas técnicos y resolver todas sus solicitudes de TI en un instante. "
        "¿Tiene alguna inquietud? Simplemente responda a este correo electrónico y nos pondremos en contacto. Gracias!\n"
        "Esta mesa de ayuda funciona con Workspace. No utilizamos ninguna información personal que agregue a su(s) Ticket(s). "
        "Utilizamos su información personal para proporcionar los servicios de la mesa de ayuda. Términos de uso | política de privacidad"
    )

    html_content = (
        f"<h2><strong>Hola, {email}!</strong></h2>"
        "<p>Usted ha sido invitado a realizar inicio de sesión en el portal CRM Mesa de Ayuda.</p>"
        f"<p><a href='{settings.SITE_URL}/portal/access/{token}/'>Click en el link para iniciar sesión en el Portal</a></p>"
        "<p>El enlace de invitación anterior es válido solo por un corto período de tiempo, así que inicie sesión rápidamente.</p>"
        "<p>Gracias por Contactarnos!</p>"
        "<hr>"
        "<p><strong>¿Por qué recibió este correo electrónico?</strong> ¡Me alegra que hayas preguntado! Estamos usando Workspace IT mesa de ayuda para rastrear problemas técnicos y resolver todas sus solicitudes de TI en un instante. "
        "¿Tiene alguna inquietud? Simplemente responda a este correo electrónico y nos pondremos en contacto. Gracias!</p>"
        "<p>Esta mesa de ayuda funciona con Workspace. No utilizamos ninguna información personal que agregue a su(s) Ticket(s). "
        "Utilizamos su información personal para proporcionar los servicios de la mesa de ayuda. <a href='#'>Términos de uso</a> | <a href='#'>política de privacidad</a></p>"
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_admin_login_email(email):
    subject = 'Inicie sesión en el portal de su mesa de ayuda'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]
    
    text_content = (
        f"Hola, {email}\n\n"
        "Su dirección de correo electrónico se utilizó recientemente para solicitar un enlace de inicio de sesión para CRM. "
        "Los administradores no pueden iniciar sesión a través del portal y, en su lugar, deben iniciar sesión desde la página de inicio de sesión del servicio de asistencia.\n\n"
        "Gracias por Contactarnos!\n"
        "---------------------------------------------------------------------------------\n"
        "¿Por qué recibió este correo electrónico? ¡Me alegra que hayas preguntado! Estamos usando Workspace IT mesa de ayuda para rastrear problemas técnicos y resolver todas sus solicitudes de TI en un instante. "
        "¿Tiene alguna inquietud? Simplemente responda a este correo electrónico y nos pondremos en contacto. Gracias!\n"
        "Esta mesa de ayuda funciona con workspace. No utilizamos ninguna información personal que agregue a su(s) Ticket(s). "
        "Utilizamos su información personal para proporcionar los servicios de la mesa de ayuda. Términos de uso | política de privacidad"
    )

    html_content = (
        f"<h2><strong>Hola, {email}!</strong></h2>"
        "<p>Su dirección de correo electrónico se utilizó recientemente para solicitar un enlace de inicio de sesión para CRM. "
        "Los administradores no pueden iniciar sesión a través del portal y, en su lugar, deben iniciar sesión desde la página de inicio de sesión del <a href='#'>servicio de asistencia.</a></p>"
        "<p>Gracias por Contactarnos!</p>"
        "<hr>"
        "<p><strong>¿Por qué recibió este correo electrónico?</strong> ¡Me alegra que hayas preguntado! Estamos usando Workspace IT mesa de ayuda para rastrear problemas técnicos y resolver todas sus solicitudes de TI en un instante. "
        "¿Tiene alguna inquietud? Simplemente responda a este correo electrónico y nos pondremos en contacto. Gracias!</p>"
        "<p>Esta mesa de ayuda funciona con workspace. No utilizamos ninguna información personal que agregue a su(s) Ticket(s). "
        "Utilizamos su información personal para proporcionar los servicios de la mesa de ayuda. <a href='#'>Términos de uso</a> | <a href='#'>política de privacidad</a></p>"
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()