from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction

from plants.models import Comment
from .models import Profile
from .forms import SignUpForm

# Create your views here.

def sign_up(request: HttpRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.save()

                avatar = form.cleaned_data.get("avatar") or "images/avatars/avatar.png"
                about = form.cleaned_data.get("about", "")

                Profile.objects.create(
                    user=user,
                    about=about,
                    avatar=avatar
                )

            messages.success(request, "Registered successfully")
            return redirect("accounts:sign_in")

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def sign_in(request:HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully")
    return redirect("main:home")


def user_profile_view(request: HttpRequest, user_name):
    user = get_object_or_404(User, username=user_name)

    Profile.objects.get_or_create(user=user)

    comments = Comment.objects.filter(user=user).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        "user": user,
        "comments": comments
    })


def update_user_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("accounts:sign_in")
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                user = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile = user.profile
                profile.about = request.POST.get("about", "")

                if "avatar" in request.FILES:
                    profile.avatar = request.FILES["avatar"]

                profile.save()
            messages.success(request, "updated profile successfully")
        except Exception as e:
            messages.error(request, "Couldn't update profile")
            print(e)

        return redirect("accounts:user_profile_view", user_name=user.username)

    return render(request, "accounts/update_profile.html")



