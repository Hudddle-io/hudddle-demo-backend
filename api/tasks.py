from celery import shared_task
from django.core.mail import send_mail
    
# @shared_task
def send_huddle_ready_email(email):
    subject = "Your huddle demo account is ready"
    message = "Hello, your huddle demo account is ready. Please click the link below to get started."
    from_email = "hudddle.ioo@gmail.com"
    
    send_mail(subject, message, from_email, [email], fail_silently=False)