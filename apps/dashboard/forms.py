from django import forms
from weblog.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'slug': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'laisser-vide-pour-auto-generer'}),
        }
