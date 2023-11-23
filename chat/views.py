from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.contrib.auth import login as create_token
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.urls import reverse
from .models import Bot, Conversation, Message
from .forms import ChatForm
from pgvector.django import L2Distance

from .utilities import (
    get_prompt,
    get_conversation_title,
    chat,
    get_embedding,
)


def text_search(query: str):
    vector = SearchVector('message')
    search_query = SearchQuery(query)
    return (
        Message.objects.annotate(rank=SearchRank(vector, search_query))
        .filter(rank__gte=0.001)
        .order_by("-rank")
    )


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
    bot_list = Bot.objects.filter(creator=request.user)
    conversations_list = Conversation.objects.all()
    query = request.GET.get("query")
    if query:
        messages_list = text_search(query).filter(creator=request.user)

    return render(
        request,
        "chat-list.html",
        {
            "bot_list": bot_list,
            "conversations_list": conversations_list,
            "messages_list": messages_list
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
    else:
        chatbot = Bot.objects.get(pk=-id)
        conversation = Conversation(bot=chatbot, title="DEFAULT")
        conversation.save()

    if request.method != "POST":
        form = ChatForm()
        return render(
            request, "chat-details.html", {"form": form, "conversation": conversation}
        )

    form = ChatForm(request.POST)
    if not form.is_valid():
        raise Http404("Please fill the form properly")

    embedding = get_embedding(form.cleaned_data["query"])
    nearby_documents = (
        Bot.objects.order_by(L2Distance("document_vector", embedding))
        .first()
        .document_text
    )
    prompt = get_prompt(context=nearby_documents, query=form.cleaned_data["query"])

    if conversation.title == "DEFAULT":
        conversation.title = get_conversation_title(form.cleaned_data["query"])
        conversation.save()

    chat_completion = chat(prompt, frequence_penalty=1)

    user_message = Message(
        message=form.cleaned_data["query"], conversation=conversation
    )
    user_message.save()
    bot_message = Message(
        message=chat_completion.choices[0].message.content,
        conversation=conversation,
    )
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
