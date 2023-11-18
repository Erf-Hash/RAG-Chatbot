import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth import authenticate, login as create_token
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Bot, Conversation, Message
from .forms import ChatForm
from openai import OpenAI


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
    return redirect(reverse("chat_list"))


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
def chat_list(request: HttpRequest):
    PAGE_LENGTH = 10

    context = {"1": "SALAM", "2": "KHOOBI", "3": "CHEKHABAR"}
    bot_list = Bot.objects.all()
    conversations_list = Conversation.objects.all()

    return render(
        request,
        "chat-list.html",
        {
            "bot_list": bot_list,
            "conversations_list": conversations_list,
        },
    )


@login_required
def create_chat(request: HttpRequest):
    return render(request, "create-chat.html")


@login_required
def chat_details(request: HttpRequest, id: int):
    id = int(id)
    if id > 0:
        conversation = Conversation.objects.get(pk=id)
        chatbot = conversation.bot
        conversation.save()
    else:
        chatbot = Bot.objects.get(pk=-id)
        conversation = Conversation.objects.get(bot=chatbot)
        chatbot.save()

    if request.method != "POST":
        form = ChatForm()
        return render(request, "chat-details.html", {"form": form, "conversation": conversation})
    

    form = ChatForm(request.POST)
    if not form.is_valid():
        raise Http404("Please fill the form properly")

    client = OpenAI(
        api_key="C9vpBLBZkAbvbvimiOogyxJ8bOiLRkv3",
        base_url="https://openai.torob.ir/v1",
    )
    chat_completion = json.loads(
        client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": form.cleaned_data["query"],
                },
            ],
            model="gpt-3.5-turbo",
            frequency_penalty=0,
            n=1,
        )
    )

    user_message = Message(message=form.cleaned_data["query"])
    user_message.save()
    bot_message = Message(message=chat_completion["choices"][0]["message"]["content"])
    bot_message.save()

    # add messages to conversation

    return render(
        request,
        "chat-details.html",
        {
            "form": form,
            "responses": bot_message.message,
        },
    )
