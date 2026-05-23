from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('articles/new/', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_update, name='article_update'),
    path('comments/', views.comment_list, name='comment_list'),
    path('comments/<int:pk>/toggle-active/', views.comment_toggle_active, name='comment_toggle_active'),
    path('subscribers/', views.subscriber_list, name='subscriber_list'),
    path('subscribers/<int:pk>/toggle-active/', views.subscriber_toggle_active, name='subscriber_toggle_active'),
    path('media/', views.media_library, name='media_library'),
    path('analytics/', views.analytics, name='analytics'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('recruitment/', views.promotion_request, name='promotion_request'),
    path('recruitment/manage/', views.promotion_request_list, name='promotion_request_list'),
    path('recruitment/<int:pk>/<str:action>/', views.promotion_request_handle, name='promotion_request_handle'),
]
