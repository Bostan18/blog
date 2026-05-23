from django import forms
from .models import CustomUser, PromotionRequest

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'twitter_url', 'linkedin_url', 'facebook_url', 'website_url', 'show_recruitment_section']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'twitter_url': forms.URLInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'facebook_url': forms.URLInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'website_url': forms.URLInput(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'show_recruitment_section': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500'}),
        }

class PromotionRequestForm(forms.ModelForm):
    class Meta:
        model = PromotionRequest
        fields = ['requested_role', 'message']
        widgets = {
            'requested_role': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none'}),
            'message': forms.Textarea(attrs={'rows': 5, 'class': 'w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'Expliquez pourquoi vous souhaitez ce rôle et ce que vous pouvez apporter au journal...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On limite les choix de rôles pour ne pas pouvoir postuler à Admin ou Visiteur
        valid_roles = [
            (CustomUser.Role.WRITER, "Rédacteur"),
            (CustomUser.Role.EDITOR, "Éditeur"),
        ]
        self.fields['requested_role'].choices = valid_roles
