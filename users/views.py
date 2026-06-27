from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # заполняем форму данными из запроса
        if form.is_valid():  # Django проверяет валидность
            user = form.save()  # создаёт пользователя в БД
            login(request, user)  # создаёт сессию в Redis
            return redirect("/")  # редирект на главную
    else:
        form = UserCreationForm()  # пустая форма для GET запроса

    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")
