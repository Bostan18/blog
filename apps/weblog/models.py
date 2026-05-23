from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status='PUBLISHED',
            published_at__lte=timezone.now()
        )

class Category(models.Model):
    name = models.CharField(_("Nom"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=120)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(_("Nom"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, max_length=70)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Brouillon")
        PUBLISHED = "PUBLISHED", _("Publié")
        ARCHIVED = "ARCHIVED", _("Archivé")

    title = models.CharField(_("Titre"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, max_length=255)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name=_("Auteur")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name=_("Catégorie")
    )
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True, verbose_name=_("Tags"))
    
    content = models.TextField(_("Contenu"))
    excerpt = models.TextField(_("Extrait"), max_length=500, blank=True)
    featured_image = models.ImageField(_("Image à la une"), upload_to="articles/", null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(_("Méta-titre"), max_length=100, blank=True, help_text=_("Titre pour les moteurs de recherche (SEO)"))
    meta_description = models.TextField(_("Méta-description"), max_length=160, blank=True, help_text=_("Description pour les moteurs de recherche (SEO)"))
    
    status = models.CharField(
        _("Statut"),
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)
    published_at = models.DateTimeField(_("Publié le"), null=True, blank=True)
    
    # Analytics
    views_count = models.PositiveIntegerField(_("Nombre de vues"), default=0)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
