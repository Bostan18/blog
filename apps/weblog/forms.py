from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 'category', 'tags', 'content', 'excerpt', 
            'featured_image', 'status', 'published_at',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'id': 'richtext-editor'}),
        }
