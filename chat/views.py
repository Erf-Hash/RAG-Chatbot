from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def login(request: HttpRequest):
    if request.method == "GET":
        return render(request, "login.html")

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is None:
        raise Http404()

    login(request, user)
    return redirect("/")


def register(request):
    return render(request, 'register.html')


@login_required
def test(request):
    pass
