from django.urls import path
from . import views
from .feeds import LatestArticlesFeed

app_name = 'weblog'

urlpatterns = [
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('chroniques/', views.chronique_list, name='chronique_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('authors/', views.author_index, name='author_index'),
    path('author/<str:username>/', views.author_detail, name='author_detail'),
    path('rss/', LatestArticlesFeed(), name='article_feed'),
]
