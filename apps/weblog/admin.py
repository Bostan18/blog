from django.contrib import admin
from .models import Category, Tag, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "created_at", "published_at"]
    list_filter = ["status", "category", "tags", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    raw_id_fields = ["author"]
    date_hierarchy = "published_at"
