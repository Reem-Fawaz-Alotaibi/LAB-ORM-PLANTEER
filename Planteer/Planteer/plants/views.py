
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpRequest
from .models import Plant,Comment,Country
from .forms import PlantForm
from django.contrib import messages
from accounts.models import Bookmark

def all_plants_view(request):
    plants = Plant.objects.all().order_by('-created_at')
    countries = Country.objects.all()

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country = request.GET.get('country')

    if category:
        plants = plants.filter(category=category)

    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    if country:
        plants = plants.filter(countries__id=country)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'countries': countries
    })


def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    comments = Comment.objects.filter(plant=plant).order_by("-created_at")
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

    is_bookmarked = False

    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user,
            plant=plant
        ).exists()

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'comments': comments,
        'related_plants': related_plants,
        'is_bookmarked': is_bookmarked,

    })


def new_plant_view(request):
    if not request.user.is_staff:
        messages.warning(request, "only staff can add game", "alert-warning")
        return redirect("main:home")

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm()

    return render(request, 'plants/new_plant.html', {'form': form})


def update_plant_view(request, plant_id):
    if not request.user.is_staff:
      messages.warning(request, "only staff can add game", "alert-warning")
      return redirect("main:home")
   
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {
        'form': form,
        'plant': plant
    })


def delete_plant_view(request, plant_id):
    if not request.user.is_staff:
      messages.warning(request, "only staff can add game", "alert-warning")
      return redirect("main:home")

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('plants:all_plants')

    return render(request, 'plants/delete_plant.html', {'plant': plant})


def search_plants_view(request):
    query = request.GET.get('q', '')
    plants = []

    if query:
        plants = Plant.objects.filter(name__istartswith=query)

    return render(request, 'plants/search_plants.html', {
        'plants': plants,
        'query': query
    })


def add_comment_view(request: HttpRequest, plant_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add comment")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        plant_object = Plant.objects.get(pk=plant_id)
        new_comment = Comment(
            plant=plant_object,
            user=request.user,
            comment=request.POST["comment"]
        )
        new_comment.save()
        messages.success(request, "Added Comment Successfully", "alert-success")
    return redirect("plants:plant_detail", plant_id=plant_id)


def country_plants_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    plants = Plant.objects.filter(countries=country).distinct()
    context = {
        'country': country,
        'plants': plants,
    }
    return render(request, 'plants/country_plants.html', context)


def bookmark_view(request: HttpRequest, plant_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered users can add bookmarks")
        return redirect("accounts:sign_in")
    try:
        plant = Plant.objects.get(pk=plant_id)

        bookmark = Bookmark.objects.filter(plant=plant, user=request.user).first()

        if not bookmark:
            Bookmark.objects.create(user=request.user, plant=plant)
            messages.success(request, "Bookmark added")
        else:
            bookmark.delete()
            messages.warning(request, "Bookmark removed")

    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong")

    return redirect("plants:plant_detail", plant_id=plant_id)