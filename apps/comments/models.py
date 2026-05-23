from django.db import models
from django.conf import settings
from weblog.models import Article
from django.utils.translation import gettext_lazy as _

class Comment(models.Model):
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name="comments",
        verbose_name=_("Article")
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Auteur")
    )
    content = models.TextField(_("Commentaire"), max_length=1000)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)
    is_active = models.BooleanField(_("Actif"), default=True)

    class Meta:
        verbose_name = _("Commentaire")
        verbose_name_plural = _("Commentaires")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.article.title}"
