from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth import authenticate, login as create_token
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Bot, Conversation


def login(request: HttpRequest):
    if request.GET.get("email") is None:
        return render(request, "login.html")

    email = request.GET["email"]
    password = request.GET["password"]

    user = User.objects.get(email=email)
    print(user)
    if user is None or user.check_password(password):
        raise Http404()

    create_token(request, user)
    return redirect(reverse('chat_list', kwargs={'page': 0}))


def register(request: HttpRequest):
    if request.GET.get("email") is None:
        return render(request, "register.html")

    email = request.GET["email"]
    password = request.GET["password"]
    password_confirm = request.GET["password-confirm"]

    if password != password_confirm:
        raise Http404()

    user = User(username=email, password=password, email=email)
    user.save()

    return redirect("login")


@login_required
def chat_list(request: HttpRequest, page: int = 0):
    PAGE_LENGTH = 10

    bot_list = Bot.objects.all()
    conversations_list = Conversation.objects.all()[page * PAGE_LENGTH: page * PAGE_LENGTH + PAGE_LENGTH]


    return render(request, "chat-list.html")


@login_required
def create_chat(request: HttpRequest):
    return render(request, "create-chat.html")


@login_required
def chat_details(request: HttpRequest):
    return render(request, "chat-details.html")
