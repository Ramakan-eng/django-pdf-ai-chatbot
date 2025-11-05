from django.shortcuts import render

# Create your views here.




from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.chatbot import ask_question
from .models import Conversation

# 1️⃣ Send message & get bot response
@api_view(["POST"])
def chat_with_bot(request):
    user_id = request.data.get("user_id")
    message = request.data.get("message")

    if not user_id or not message:
        return Response({"error": "user_id and message required"}, status=400)

    # Bot generates answer
    bot_response = ask_question(message)

    # Save conversation in DB
    Conversation.objects.create(
        user_id=user_id,
        user_message=message,
        bot_response=bot_response
    )

    return Response({
        "user_id": user_id,
        "user_message": message,
        "bot_response": bot_response
    })


# 2️⃣ Fetch full chat history for a given user
@api_view(["GET"])
def get_chat_history(request, user_id):
    chats = Conversation.objects.filter(user_id=user_id).order_by("timestamp")
    history = [
        {
            "conversation_id": chat.conversation_id,
            "user_message": chat.user_message,
            "bot_response": chat.bot_response,
            "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for chat in chats
    ]
    return Response({"user_id": user_id, "history": history})







# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .utils.chatbot import ask_question
# from .models import Conversation


# @api_view(["POST"])
# def chat_with_bot(request):
#     user_id = request.data.get("user_id")
#     message = request.data.get("message")

#     if not user_id or not message:
#         return Response({"error": "user_id and message required"}, status=400)

#     bot_response = ask_question(message)

#     # save to DB
#     Conversation.objects.create(
#         user_id=user_id,
#         user_message=message,
#         bot_response=bot_response
#     )

#     return Response({
#         "user_id": user_id,
#         "user_message": message,
#         "bot_response": bot_response
#     })





# @api_view(["GET"])
# def get_chat_history(request):
#     user_id = request.query_params.get("user_id")

#     if user_id:
#         chats = Conversation.objects.filter(user_id=user_id).order_by("-timestamp")
#     else:
#         chats = Conversation.objects.all().order_by("-timestamp")

#     data = [
#         {
#             "user_id": chat.user_id,
#             "user_message": chat.user_message,
#             "bot_response": chat.bot_response,
#             "timestamp": chat.timestamp
#         }
#         for chat in chats
#     ]
#     return Response(data)




import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .utils.chatbot import create_vectorstore

UPLOAD_DIR = "media/uploads"  # directory to store PDFs
os.makedirs(UPLOAD_DIR, exist_ok=True)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_pdf(request):
    """
    Upload a PDF file and create a vectorstore for it.
    """
    pdf_file = request.FILES.get("file")

    if not pdf_file:
        return Response({"error": "No PDF file uploaded"}, status=400)

    # Save uploaded file
    pdf_path = os.path.join(UPLOAD_DIR, pdf_file.name)
    with open(pdf_path, "wb+") as destination:
        for chunk in pdf_file.chunks():
            destination.write(chunk)

    # Create vectorstore from uploaded PDF
    create_vectorstore(pdf_path)

    return Response({"message": f"✅ PDF uploaded and vectorstore created for {pdf_file.name}!"})

