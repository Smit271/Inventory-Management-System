from celery import shared_task
from django.core.mail import send_mail
from inventory import settings


@shared_task(bind=True)
def send_mail_func(self, email_address, subject, message):
    mail_subject = 'Hi! Celery Testing'
    message = '''
                This is testing email from django by-default smtp settings
                Please ignore this email as per now, because we are building
                one empire of an IT company which will soon be under top 10 
                companies.
            '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_address],
        fail_silently=True
    )
    return "Done"
