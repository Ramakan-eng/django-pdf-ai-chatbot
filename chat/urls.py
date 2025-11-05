from django.urls import path
from .views import chat_with_bot, get_chat_history, upload_pdf

urlpatterns = [
    path("chat/", chat_with_bot, name="chat"),
    path("upload/", upload_pdf, name="upload"),
    path("history/<str:user_id>/", get_chat_history, name="history"),
]









# from django.urls import path
# from .views import chat_with_bot,get_chat_history,upload_pdf

# urlpatterns = [
#     path("chat/", chat_with_bot, name="chat"),
#     path("history/",get_chat_history,name='history'),
#     path('upload/',upload_pdf,name="pdf")
# ]