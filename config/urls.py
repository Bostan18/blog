from django.contrib import admin
from django.urls import path, include
from core.views import home, htmx_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('htmx-test/', htmx_test, name='htmx_test'),
    path('blog/', include('weblog.urls')),
    path('comments/', include('comments.urls')),
    path('search/', include('search.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
]
