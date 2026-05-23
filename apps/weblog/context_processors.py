from .models import Category

def categories_processor(request):
    # On exclut 'Chronique' de la navigation principale car elle a son propre lien
    categories = Category.objects.exclude(name='Chronique').order_by('name')[:6]
    return {'nav_categories': categories}
