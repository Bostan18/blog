from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        VISITOR = "VISITOR", _("Visiteur")
        CONTRIBUTOR = "CONTRIBUTOR", _("Contributeur")
        WRITER = "WRITER", _("Rédacteur")
        EDITOR = "EDITOR", _("Éditeur")
        ADMIN = "ADMIN", _("Administrateur")

    role = models.CharField(
        _("Rôle"),
        max_length=20,
        choices=Role.choices,
        default=Role.CONTRIBUTOR
    )
    bio = models.TextField(_("Biographie"), max_length=500, blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to="avatars/", null=True, blank=True)
    
    # Social links
    twitter_url = models.URLField(_("Lien Twitter/X"), max_length=255, blank=True)
    linkedin_url = models.URLField(_("Lien LinkedIn"), max_length=255, blank=True)
    facebook_url = models.URLField(_("Lien Facebook"), max_length=255, blank=True)
    website_url = models.URLField(_("Site web personnel"), max_length=255, blank=True)
    
    # Preferences
    show_recruitment_section = models.BooleanField(_("Afficher la section recrutement"), default=True)

    def __str__(self):
        return self.username

    @property
    def is_editor(self):
        return self.role == self.Role.EDITOR or self.is_staff

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

class PromotionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("En attente")
        APPROVED = "APPROVED", _("Approuvée")
        REJECTED = "REJECTED", _("Rejetée")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="promotion_requests")
    requested_role = models.CharField(_("Rôle demandé"), max_length=20, choices=CustomUser.Role.choices)
    message = models.TextField(_("Lettre de motivation"), max_length=1000)
    status = models.CharField(_("Statut"), max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Demande de promotion")
        verbose_name_plural = _("Demandes de promotion")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Demande de {self.user.username} pour le rôle {self.requested_role}"
