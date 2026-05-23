from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:article_id>/', views.add_comment, name='add_comment'),
    path('list/<int:article_id>/', views.comment_list, name='comment_list'),
]
