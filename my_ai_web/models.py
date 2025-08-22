from django.db import models
from django.utils import timezone

# Create your models here.

class ChatMessage(models.Model):
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')}: {self.user_message[:50]}..."
