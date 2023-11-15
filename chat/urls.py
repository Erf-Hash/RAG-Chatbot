from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_func),
    path('login', views.login),
    path('register', views.register),
]