from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('chat-list/<int:page>', views.chat_list, name='chat_list'),
    path('create-chat', views.create_chat, name='create_chat'),
    path('chat-details', views.chat_details, name='chat_details'),
]