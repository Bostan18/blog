from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from weblog.models import Article
from .models import Comment
from .forms import CommentForm

def comment_list(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.filter(is_active=True)
    return render(request, 'comments/partials/comment_list.html', {'comments': comments, 'article': article})

@login_required
@require_POST
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        
        # On renvoie la liste mise à jour via HTMX
        comments = article.comments.filter(is_active=True)
        return render(request, 'comments/partials/comment_list.html', {
            'comments': comments, 
            'article': article,
            'comment_success': True
        })
    
    return render(request, 'comments/partials/comment_form.html', {'form': form, 'article': article})
