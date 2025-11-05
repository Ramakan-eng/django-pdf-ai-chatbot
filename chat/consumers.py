import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.utils.chatbot import ask_question
from chat.models import Conversation
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            "message": f"✅ Connected to chat room: {self.user_id}"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming message"""
        try:
            data = json.loads(text_data)
            user_message = data.get("message", "")

            if not user_message:
                await self.send(text_data=json.dumps({"error": "Empty message"}))
                return

            # 🔹 Step 1: Generate reply from chatbot
            bot_reply = await sync_to_async(ask_question)(user_message)

            # 🔹 Step 2: Save to DB
            await self.save_message(self.user_id, user_message, bot_reply)

            # 🔹 Step 3: Send response back
            await self.send(text_data=json.dumps({
                "user_id": self.user_id,
                "user_message": user_message,
                "bot_response": bot_reply
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                "error": str(e)
            }))

    @sync_to_async
    def save_message(self, user_id, user_message, bot_response):
        Conversation.objects.create(
            user_id=user_id,
            user_message=user_message,
            bot_response=bot_response
        )
