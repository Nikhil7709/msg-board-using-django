from django.db import models
from users.models import User

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='user_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = '02. Messages'

    def __str__(self):
        return f'{self.user.email[:15]}: {self.content[:30]}'
