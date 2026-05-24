from .models import ActivityLog

def log_activity(user, action, description=""):
    """
    Utility function to log an activity.
    """
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description
    )
