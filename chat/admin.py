from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_message", "bot_response", "timestamp")
