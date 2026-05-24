from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import PromotionRequest
from weblog.models import Article
from comments.models import Comment
from .models import Notification
from .tasks import send_notification_email_task

@receiver(post_save, sender=PromotionRequest)
def notify_promotion_status(sender, instance, created, **kwargs):
    if not created: # Status changed
        if instance.status == 'APPROVED':
            title = "Félicitations !"
            msg = f"Votre demande de promotion pour le rôle {instance.requested_role} a été approuvée."
            Notification.objects.create(
                user=instance.user,
                notification_type=Notification.Type.PROMOTION,
                title=title,
                message=msg,
                link="/dashboard/"
            )
            send_notification_email_task.delay(instance.user.id, title, msg)
        elif instance.status == 'REJECTED':
            title = "Demande de promotion"
            msg = "Votre demande de promotion a été refusée pour le moment."
            Notification.objects.create(
                user=instance.user,
                notification_type=Notification.Type.PROMOTION,
                title=title,
                message=msg,
                link="/dashboard/recruitment/"
            )
            send_notification_email_task.delay(instance.user.id, title, msg)

@receiver(post_save, sender=Article)
def notify_article_published(sender, instance, created, **kwargs):
    if not created:
        # Check if status changed to PUBLISHED
        # This is simplified, ideally compare with previous value
        if instance.status == 'PUBLISHED':
             # Notify author if not the one who saved? 
             # Actually, notify followers or just log for now
             pass
    elif instance.status == 'SUBMITTED':
        # Notify editors/admins
        from users.models import CustomUser
        editors = CustomUser.objects.filter(role__in=['EDITOR', 'ADMIN'])
        for editor in editors:
            Notification.objects.create(
                user=editor,
                notification_type=Notification.Type.ARTICLE,
                title="Nouvel article à valider",
                message=f"'{instance.title}' par {instance.author.username} attend votre validation.",
                link="/dashboard/articles/pending/"
            )

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    if created and instance.article.author != instance.user:
        title = "Nouveau commentaire"
        msg = f"{instance.user.username} a commenté votre article '{instance.article.title}'."
        Notification.objects.create(
            user=instance.article.author,
            notification_type=Notification.Type.COMMENT,
            title=title,
            message=msg,
            link=f"/blog/{instance.article.slug}/"
        )
        send_notification_email_task.delay(instance.article.author.id, title, msg)
