import os
import sys
import django
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model

# Add the project directory to sys.path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from weblog.models import Category, Article, Tag

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # 1. Ensure a superuser exists
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        print("Created superuser 'admin'")

    # 2. Categories
    categories_names = [
        "Politique", "Économie", "Monde", "Culture", "Environnement", 
        "Société", "Sciences", "International", "Chronique"
    ]
    categories = {}
    for name in categories_names:
        cat, created = Category.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
        categories[name] = cat
        if created:
            print(f"Created category: {name}")

    # 3. Tags
    tags_names = ["Réforme", "Démocratie", "Innovation", "Climat", "Cinéma", "IA"]
    tags = []
    for name in tags_names:
        tag, created = Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
        tags.append(tag)
        if created:
            print(f"Created tag: {name}")

    # 4. Articles
    articles_data = [
        {
            "title": "Réforme des institutions : le projet de loi qui divise l'Assemblée nationale",
            "category": "Politique",
            "excerpt": "Le texte soumis au vote ce mardi suscite de vifs débats entre les groupes parlementaires. Analyse d'une réforme aux multiples enjeux pour la démocratie française.",
            "content": "Le gouvernement a présenté ce mardi un projet de loi ambitieux visant à réformer en profondeur les institutions de la Ve République. Ce texte, longuement attendu depuis les États généraux de la démocratie tenus en 2025, propose notamment la création d'une chambre citoyenne, la modification du mode de scrutin législatif et une révision des pouvoirs du Conseil constitutionnel.\n\nLa séance d'examen en commission des lois a donné lieu à des échanges particulièrement vifs entre les différents groupes parlementaires. La majorité défend un texte « historique » qui permettra de « redonner du pouvoir au peuple », tandis que l'opposition dénonce une « réforme cosmétique » qui ne répond pas aux enjeux démocratiques contemporains.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Inflation : les prix de l'énergie en forte baisse ce trimestre",
            "category": "Économie",
            "excerpt": "Les tarifs de l'électricité et du gaz amorcent une décrue significative, apportant un souffle d'air frais aux ménages et aux entreprises.",
            "content": "Après des mois de tensions sur les marchés mondiaux, les prix de l'énergie affichent une baisse marquée. Cette tendance, portée par une production renouvelable record et une demande stabilisée, devrait se confirmer dans les mois à venir selon les experts.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Canicules : un plan d'adaptation présenté par le gouvernement",
            "category": "Environnement",
            "excerpt": "Face à l'intensification des vagues de chaleur, de nouvelles mesures sont annoncées pour protéger les populations vulnérables et adapter les infrastructures.",
            "content": "Le ministre de la Transition écologique a dévoilé ce matin le plan 'Horizon Frais'. Au programme : végétalisation massive des centres-villes, rénovation thermique des bâtiments publics et renforcement des systèmes de veille sanitaire.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Festival de Cannes : la sélection officielle dévoilée",
            "category": "Culture",
            "excerpt": "Le plus grand festival de cinéma au monde a révélé les films qui concourront pour la Palme d'Or cette année.",
            "content": "C'est un cru exceptionnel qui s'annonce sur la Croisette. Entre grands maîtres et jeunes talents prometteurs, la sélection officielle promet de grands moments de cinéma et de débats passionnés.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "« La démocratie ne se préserve pas, elle se pratique »",
            "category": "Chronique",
            "excerpt": "Face à la montée des populismes en Europe, il est temps de repenser notre rapport à la citoyenneté et à l'engagement politique.",
            "content": "Face à la montée des populismes en Europe et à la défiance croissante envers les institutions représentatives, il est temps de repenser notre rapport à la citoyenneté. La réponse ne viendra pas d'un homme providentiel, mais d'une participation renouvelée de chacun.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Cinéma et politique : quand le 7e art reflète nos fractures",
            "category": "Chronique",
            "excerpt": "De « Les Misérables » à « Anatomie d'une chute », le cinéma français interroge notre société avec une acuité renouvelée.",
            "content": "Le cinéma a toujours été un miroir de la société. Aujourd'hui plus que jamais, les réalisateurs s'emparent des sujets brûlants pour susciter la réflexion et parfois le débat national.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Intelligence artificielle : la Commission européenne propose un cadre réglementaire",
            "category": "Sciences",
            "excerpt": "Un texte pionnier pour encadrer le développement de l'IA tout en favorisant l'innovation sur le continent.",
            "content": "L'Europe souhaite devenir le leader de l'IA éthique. Le nouveau projet de règlement classe les systèmes d'IA par niveau de risque, imposant des contraintes strictes aux applications jugées sensibles.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Espace : la mission Artemis III annonce sa date de lancement",
            "category": "Sciences",
            "excerpt": "Le retour de l'humanité sur la Lune se précise avec une fenêtre de tir désormais fixée pour fin 2026.",
            "content": "La NASA et ses partenaires internationaux ont confirmé que les préparatifs avancent selon le calendrier prévu. Artemis III marquera une étape historique avec la première femme à marcher sur le sol lunaire.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Tensions au Moyen-Orient : diplomatie et sanctions au cœur des débats",
            "category": "International",
            "excerpt": "Le sommet extraordinaire de l'ONU tente de trouver une issue pacifique aux récents affrontements frontaliers.",
            "content": "La communauté internationale est mobilisée pour éviter une escalade régionale. Les discussions de coulisses s'intensifient entre les grandes puissances pour proposer une feuille de route de désescalade.",
            "status": Article.Status.PUBLISHED,
        },
        {
            "title": "Sommet européen : les chefs d'État s'accordent sur un nouveau pacte climatique",
            "category": "Monde",
            "excerpt": "Un accord qualifié d'historique pour accélérer la réduction des émissions de gaz à effet de serre à l'échelle du continent.",
            "content": "Après 48 heures de négociations acharnées, les 27 ont trouvé un compromis ambitieux. Le nouveau pacte prévoit des investissements massifs dans les énergies décarbonées et une taxation accrue des produits importés à forte empreinte carbone.",
            "status": Article.Status.PUBLISHED,
        }
    ]

    for data in articles_data:
        article, created = Article.objects.get_or_create(
            title=data["title"],
            defaults={
                "slug": slugify(data["title"]),
                "author": admin_user,
                "category": categories[data["category"]],
                "excerpt": data["excerpt"],
                "content": data["content"],
                "status": data["status"],
                "published_at": timezone.now()
            }
        )
        if created:
            article.tags.add(*tags[:2])
            print(f"Created article: {article.title}")

    print("Sample data creation complete!")

if __name__ == "__main__":
    create_sample_data()
