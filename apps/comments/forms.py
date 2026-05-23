from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-indigo-500 transition-all duration-200 bg-gray-50 resize-none',
                'placeholder': 'Laissez un commentaire...',
                'rows': '3',
            }),
        }
