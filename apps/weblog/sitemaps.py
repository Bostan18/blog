from django.contrib.sitemaps import Sitemap
from .models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        from django.urls import reverse
        return reverse('weblog:category_detail', kwargs={'slug': obj.slug})
