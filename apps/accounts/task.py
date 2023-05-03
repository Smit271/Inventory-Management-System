from celery import shared_task
from django.core.mail import send_mail
from inventory import settings


@shared_task(bind=True)
def send_mail_func(self, email_address, subject, message, html_message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_address],
        html_message=html_message,
        fail_silently=True
    )
    return "Done"
