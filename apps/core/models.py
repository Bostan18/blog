from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    class Type(models.TextChoices):
        PROMOTION = "PROMOTION", _("Promotion")
        ARTICLE = "ARTICLE", _("Article")
        COMMENT = "COMMENT", _("Commentaire")
        SYSTEM = "SYSTEM", _("Système")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Destinataire")
    )
    notification_type = models.CharField(
        _("Type"),
        max_length=20,
        choices=Type.choices,
        default=Type.SYSTEM
    )
    title = models.CharField(_("Titre"), max_length=255)
    message = models.TextField(_("Message"))
    link = models.CharField(_("Lien"), max_length=255, blank=True, null=True)
    is_read = models.BooleanField(_("Lu"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification pour {self.user.username} : {self.title}"

class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activity_logs",
        verbose_name=_("Utilisateur")
    )
    action = models.CharField(_("Action"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Journal d'activité")
        verbose_name_plural = _("Journaux d'activité")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action} ({self.created_at})"

