from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from weblog.models import Article
from weblog.forms import ArticleForm
from comments.models import Comment
from django.contrib import messages
from django.db.models import Sum, Avg, F
from newsletter.models import Subscriber
from users.models import PromotionRequest
from users.forms import UserProfileForm, PromotionRequestForm

def is_writer_or_admin(user):
    return user.is_authenticated and (user.role in ['WRITER', 'EDITOR', 'ADMIN'] or user.is_staff)

def is_editor_or_admin(user):
    return user.is_authenticated and (user.role in ['EDITOR', 'ADMIN'] or user.is_staff)

@login_required
def dashboard_home(request):
    if request.user.role == 'VISITOR':
        return render(request, 'dashboard/home_visitor.html')

    if request.user.is_superuser or request.user.role in ['ADMIN', 'EDITOR']:
        articles = Article.objects.all().order_by('-created_at')
    else:
        articles = Article.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'dashboard/home.html', {'articles': articles})

@login_required
@user_passes_test(is_writer_or_admin)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            messages.success(request, "L'article a été créé avec succès.")
            return redirect('dashboard:home')
    else:
        form = ArticleForm()
    
    return render(request, 'dashboard/article_form.html', {'form': form, 'title': "Créer un article"})

@login_required
@user_passes_test(is_writer_or_admin)
def article_update(request, pk):
    if request.user.is_superuser or request.user.role == 'ADMIN':
        article = get_object_or_404(Article, pk=pk)
    else:
        article = get_object_or_404(Article, pk=pk, author=request.user)
        
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "L'article a été mis à jour.")
            return redirect('dashboard:home')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'dashboard/article_form.html', {'form': form, 'article': article, 'title': "Modifier l'article"})

@login_required
@user_passes_test(is_writer_or_admin)
def comment_list(request):
    if request.user.is_superuser or request.user.role in ['ADMIN', 'EDITOR']:
        comments = Comment.objects.all().order_by('-created_at')
    else:
        comments = Comment.objects.filter(article__author=request.user).order_by('-created_at')
    
    return render(request, 'dashboard/comment_list.html', {'comments': comments})

@login_required
@user_passes_test(is_writer_or_admin)
def comment_toggle_active(request, pk):
    if request.user.is_superuser or request.user.role in ['ADMIN', 'EDITOR']:
        comment = get_object_or_404(Comment, pk=pk)
    else:
        comment = get_object_or_404(Comment, pk=pk, article__author=request.user)
    
    comment.is_active = not comment.is_active
    comment.save()
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/comment_row.html', {'comment': comment})
        
    return redirect('dashboard:comment_list')

@login_required
@user_passes_test(is_editor_or_admin)
def subscriber_list(request):
    subscribers = Subscriber.objects.all().order_by('-subscribed_at')
    return render(request, 'dashboard/subscriber_list.html', {'subscribers': subscribers})

@login_required
@user_passes_test(is_editor_or_admin)
def subscriber_toggle_active(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    subscriber.is_active = not subscriber.is_active
    subscriber.save()
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/subscriber_row.html', {'sub': subscriber})
        
    return redirect('dashboard:subscriber_list')

@login_required
@user_passes_test(is_writer_or_admin)
def media_library(request):
    articles_with_images = Article.objects.exclude(featured_image="").order_by('-created_at')
    return render(request, 'dashboard/media_library.html', {'articles': articles_with_images})

@login_required
@user_passes_test(is_writer_or_admin)
def analytics(request):
    if request.user.is_superuser or request.user.role in ['ADMIN', 'EDITOR']:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(author=request.user)
    
    total_views = articles.aggregate(Sum('views_count'))['views_count__sum'] or 0
    avg_views = articles.aggregate(Avg('views_count'))['views_count__avg'] or 0
    
    top_articles = articles.order_by('-views_count')[:10]
    
    context = {
        'total_views': total_views,
        'avg_views': avg_views,
        'top_articles': top_articles,
        'articles_count': articles.count(),
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('dashboard:profile_edit')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'dashboard/profile_edit.html', {'form': form})

from .forms import CategoryForm

@login_required
@user_passes_test(is_editor_or_admin)
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_editor_or_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La rubrique a été créée.")
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': "Créer une rubrique"})

@login_required
@user_passes_test(is_editor_or_admin)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "La rubrique a été mise à jour.")
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': "Modifier la rubrique"})

@login_required
def promotion_request(request):
    existing_request = PromotionRequest.objects.filter(user=request.user, status='PENDING').first()
    if request.method == 'POST':
        if existing_request:
            messages.warning(request, "Vous avez déjà une demande en attente.")
            return redirect('dashboard:promotion_request')
        form = PromotionRequestForm(request.POST)
        if form.is_valid():
            promo_req = form.save(commit=False)
            promo_req.user = request.user
            promo_req.save()
            messages.success(request, "Votre demande a été envoyée.")
            return redirect('dashboard:promotion_request')
    else:
        form = PromotionRequestForm()
    return render(request, 'dashboard/promotion_request.html', {
        'form': form,
        'existing_request': existing_request,
        'my_requests': PromotionRequest.objects.filter(user=request.user).order_by('-created_at')
    })

@login_required
@user_passes_test(is_editor_or_admin)
def promotion_request_list(request):
    requests = PromotionRequest.objects.all().order_by('-created_at')
    return render(request, 'dashboard/promotion_request_list.html', {'requests': requests})

@login_required
@user_passes_test(is_editor_or_admin)
def promotion_request_handle(request, pk, action):
    promo_req = get_object_or_404(PromotionRequest, pk=pk)
    if action == 'approve':
        promo_req.status = 'APPROVED'
        user = promo_req.user
        user.role = promo_req.requested_role
        user.save()
        messages.success(request, f"La demande de {user.username} a été approuvée.")
    elif action == 'reject':
        promo_req.status = 'REJECTED'
        messages.info(request, f"La demande de {promo_req.user.username} a été rejetée.")
    promo_req.save()
    return redirect('dashboard:promotion_request_list')
