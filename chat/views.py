from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth import authenticate, login as log_in
from django.contrib.auth.decorators import login_required
from .models import User


def login(request: HttpRequest):
    if request.GET.get('email') is None:
        return render(request, 'login.html')

    email = request.GET['email']
    password = request.GET['password']

    user = User.objects.get(email=email)
    print(user)
    if user is None or user.check_password(password):
        raise Http404()

    log_in(request, user)
    return HttpResponse('login was successful')


def register(request: HttpRequest):
    if request.GET.get('email') is None:
        return render(request, 'register.html')

    email = request.GET['email']
    password = request.GET['password']
    password_confirm = request.GET['password-confirm']

    if password != password_confirm:
        raise Http404()
    
    user = User(username=email, password=password, email=email)
    user.save()

    return HttpResponse('user registered successfuly')


    
    return redirect('/')


@login_required
def test_func(request):
    return HttpResponse('hello')
