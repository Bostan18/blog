from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from weblog.models import Article
from .models import Notification

@login_required
def notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, "core/partials/notification_count.html", {'unread_notifications_count': count})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, "core/partials/notification_list.html", {'notifications': notifications})

@login_required
def mark_notification_as_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
    except Notification.DoesNotExist:
        pass
    return notification_list(request)

def home(request):
    articles = Article.published.all().order_by('-published_at')
    
    # Articles pour les différentes sections
    hero_article = articles.first()
    side_articles = articles[1:4]
    latest_articles = articles[4:8]
    
    # Chroniques (catégorie spécifique)
    chroniques = Article.published.filter(
        category__name='Chronique'
    ).order_by('-published_at')[:3]
    
    # Les plus lus (simulation pour le moment)
    top_articles = articles[:5]

    context = {
        'hero_article': hero_article,
        'side_articles': side_articles,
        'latest_articles': latest_articles,
        'chroniques': chroniques,
        'top_articles': top_articles,
    }
    return render(request, "home.html", context)

def htmx_test(request):
    # Simulation d'un petit délai pour voir l'indicateur de chargement
    import time
    time.sleep(0.5)
    return render(request, "partials/htmx_test.html")
