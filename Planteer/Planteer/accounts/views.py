from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.db import IntegrityError, transaction
from plants.models import Comment

# Create your views here.

def sign_up(request: HttpRequest):

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"]
                )

                avatar = request.FILES.get("avatar")

                if not avatar:
                    avatar = "images/avatars/avatar.png"

                Profile.objects.create(
                    user=new_user,
                    about=request.POST.get("about", ""),
                    avatar=avatar
                )

            messages.success(request, "Registered User Successfully", "alert-success")
            return redirect("accounts:sign_in")

        except IntegrityError:
            messages.error(request, "Please choose another username")

        except Exception as e:
            messages.error(request, "Couldn't register user. Try again")
            print(e)

    return render(request, "accounts/signup.html", {})


def sign_in(request:HttpRequest):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong")
    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect("main:home")


def user_profile_view(request: HttpRequest, user_name):

    try:
        user = User.objects.get(username=user_name)

        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()

        comments = Comment.objects.filter(user=user).order_by('-created_at')

    except Exception as e:
        print(e)
        return render(request, '4O4.html')

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
            messages.success(request, "updated profile successfuly")
        except Exception as e:
            messages.error(request, "Couldn't update profile")
            print(e)


        return redirect("accounts:user_profile_view", user_name=user.username)

    return render(request, "accounts/update_profile.html")



