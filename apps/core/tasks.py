from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

@shared_task
def send_notification_email_task(user_id, subject, message):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        if user.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return f"Email sent to {user.email}"
    except User.DoesNotExist:
        return f"User {user_id} not found"
    except Exception as e:
        return str(e)
