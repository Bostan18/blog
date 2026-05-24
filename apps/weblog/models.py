from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from simple_history.models import HistoricalRecords

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
        SUBMITTED = "SUBMITTED", _("En attente de validation")
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

    history = HistoricalRecords()

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
        
        # Automated moderation logic (Fast-track)
        if not self.pk: # New article
            if self.status == self.Status.PUBLISHED or self.status == self.Status.SUBMITTED:
                self._apply_moderation_logic()
        else: # Existing article
            old_instance = Article.objects.get(pk=self.pk)
            if old_instance.status == self.Status.DRAFT and self.status != self.Status.DRAFT:
                self._apply_moderation_logic()

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)

    def _apply_moderation_logic(self):
        """
        Logic for trust-based auto-approval.
        - EDITOR, ADMIN publish directly.
        - WRITER with >= 3 published articles publish directly.
        - Others (CONTRIBUTOR, new WRITER) go to SUBMITTED.
        """
        from users.models import CustomUser
        user = self.author
        
        if user.is_staff or user.role in [CustomUser.Role.EDITOR, CustomUser.Role.ADMIN]:
            self.status = self.Status.PUBLISHED
        elif user.role == CustomUser.Role.WRITER:
            published_count = Article.objects.filter(author=user, status=self.Status.PUBLISHED).count()
            if published_count >= 3:
                self.status = self.Status.PUBLISHED
            else:
                self.status = self.Status.SUBMITTED
        else:
            self.status = self.Status.SUBMITTED

class FavoriteArticle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("Utilisateur")
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name=_("Article")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Article favori")
        verbose_name_plural = _("Articles favoris")
        unique_together = ('user', 'article')
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} aime {self.article}"
