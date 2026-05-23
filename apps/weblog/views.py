from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Article, Category

from django.db.models import F

def article_detail(request, slug):
    article = get_object_or_404(Article.published, slug=slug)
    
    # Incrémenter le compteur de vues
    Article.objects.filter(pk=article.pk).update(views_count=F('views_count') + 1)
    
    # Articles pour la sidebar
    latest_articles = Article.published.exclude(id=article.id).order_by('-published_at')[:5]
    recommended_articles = Article.published.filter(
        category=article.category
    ).exclude(id=article.id).order_by('-published_at')[:3]
    
    context = {
        'article': article,
        'latest_articles': latest_articles,
        'recommended_articles': recommended_articles,
    }
    return render(request, 'weblog/article_detail.html', context)

def chronique_list(request):
    User = get_user_model()
    chroniques = Article.published.filter(
        category__name='Chronique'
    ).order_by('-published_at')
    
    # Featured chronique (the latest one)
    featured_chronique = chroniques.first()
    other_chroniques = chroniques[1:] if chroniques.count() > 1 else []

    # Nos chroniqueurs (ceux qui ont écrit des chroniques)
    chroniqueurs = User.objects.filter(
        articles__category__name='Chronique',
        articles__status='PUBLISHED',
        articles__published_at__lte=timezone.now()
    ).distinct()

    context = {
        'featured_chronique': featured_chronique,
        'other_chroniques': other_chroniques,
        'chroniqueurs': chroniqueurs,
    }
    return render(request, 'weblog/chronique_list.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.published.filter(category=category).order_by('-published_at')
    
    return render(request, 'weblog/category_detail.html', {
        'category': category,
        'articles': articles
    })

def author_index(request):
    User = get_user_model()
    # On récupère les auteurs qui ont au moins un article publié
    authors = User.objects.filter(
        articles__status='PUBLISHED',
        articles__published_at__lte=timezone.now()
    ).distinct()
    return render(request, 'weblog/author_index.html', {'authors': authors})

def author_detail(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    articles = author.articles.filter(
        status='PUBLISHED',
        published_at__lte=timezone.now()
    ).order_by('-published_at')
    
    return render(request, 'weblog/author_detail.html', {
        'author': author,
        'articles': articles
    })
