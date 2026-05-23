from django.shortcuts import render
from .forms import SubscriberForm
from django.views.decorators.http import require_POST

@require_POST
def subscribe(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'newsletter/partials/success.html')
    
    # En cas d'erreur (ex: email déjà inscrit), on renvoie le formulaire avec les erreurs
    return render(request, 'newsletter/partials/form.html', {'form': form})

def newsletter_form_context(request):
    return {'subscriber_form': SubscriberForm()}
