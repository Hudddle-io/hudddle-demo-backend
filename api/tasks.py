from celery import shared_task
from django.core.mail import send_mail
    
# @shared_task
def send_huddle_ready_email(email, app_link):
    """Send an email to the user with the application link and JWT token."""
    subject = "Your huddle demo account is ready"
    message = f"Hello, your huddle demo account is ready.\n\nClick the link below to access the application:\n{app_link}\n\nBest regards,\nHudddle Team."
    from_email = "hudddle.ioo@gmail.com"
    
    send_mail(
        subject,
        message,
        from_email,
        [email],
        fail_silently=False,
    )
