from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from messagesapp.models import Message
from users.models import User


@receiver(post_save, sender=Message)
def notify_users_new_message(sender, instance, created, **kwargs):
    """Signal to notify users when a new message is created."""
    if created:
        receipient_emails = User.objects.exclude(
            id=instance.user.id
        ).values_list(
            'email', flat=True
        )
        if receipient_emails:
            send_mail(
                subject="New Message on the Board",
                message=f"{instance.user.email} posted: {instance.content}",
                from_email="jadenik13@gmail.com",
                recipient_list=list(receipient_emails),
                fail_silently=True,
            )

