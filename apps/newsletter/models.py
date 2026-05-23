from django.db import models
from django.utils.translation import gettext_lazy as _

class Subscriber(models.Model):
    email = models.EmailField(_("Email"), unique=True)
    subscribed_at = models.DateTimeField(_("Inscrit le"), auto_now_add=True)
    is_active = models.BooleanField(_("Actif"), default=True)

    class Meta:
        verbose_name = _("Abonné")
        verbose_name_plural = _("Abonnés")

    def __str__(self):
        return self.email
