from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        latest_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        return {
            'unread_notifications_count': unread_count,
            'recent_notifications': latest_notifications
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }
