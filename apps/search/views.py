from django.shortcuts import render
from django.db.models import Q
from weblog.models import Article, Category, Tag

def search_articles(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    
    articles = Article.objects.filter(status='PUBLISHED')
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).distinct()
    
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
        
    results = articles[:10]  # Limiter pour l'autocomplétion
    
    return render(request, 'search/partials/search_results.html', {
        'results': results,
        'query': query
    })

def search_page(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    
    articles = Article.objects.filter(status='PUBLISHED')
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
        
    categories = Category.objects.all()
    
    return render(request, 'search/search_page.html', {
        'articles': articles,
        'query': query,
        'categories': categories,
        'current_category': category_slug
    })
