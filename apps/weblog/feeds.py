from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article

class LatestArticlesFeed(Feed):
    title = "Le Quotidien - Derniers articles"
    link = "/blog/rss/"
    description = "Les dernières nouvelles du Quotidien."

    def items(self):
        return Article.objects.filter(status='PUBLISHED').order_by('-published_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.content[:200]

    def item_link(self, item):
        return reverse('weblog:article_detail', args=[item.slug])

    def item_pubdate(self, item):
        return item.published_at
