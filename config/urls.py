from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.views import home, htmx_test, notification_count, notification_list, mark_notification_as_read
from weblog.sitemaps import ArticleSitemap, CategorySitemap

sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('htmx-test/', htmx_test, name='htmx_test'),
    path('notifications/count/', notification_count, name='notification_count'),
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/read/<int:pk>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('blog/', include('weblog.urls')),
    path('comments/', include('comments.urls')),
    path('search/', include('search.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
