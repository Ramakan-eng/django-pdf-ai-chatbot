from django.db import models

# Create your models here.
from django.db import models

class Conversation(models.Model):
    user_id = models.CharField(max_length=100)
    conversation_id = models.AutoField(primary_key=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} - {self.user_id}"
