from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat"),
    path("test_api", views.test_api, name="test_api"),
    path("get_response", views.get_response, name="get_response"),
    path("get_chat_history", views.get_chat_history, name="get_chat_history"),
    path("clear_chat_history", views.clear_chat_history, name="clear_chat_history"),
]