
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpRequest,HttpResponse
from .models import Plant,Commint,Country
from .forms import PlantForm


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

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants
    })


def new_plant_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm()

    return render(request, 'plants/new_plant.html', {'form': form})


def update_plant_view(request, plant_id):
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

def add_commint_view(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        new_commint = Commint(
            plant=plant,
            name=request.POST["name"],
            comment=request.POST["comment"]
        )
        new_commint.save()

    return redirect('plants:plant_detail', plant_id=plant.id)

def country_plants_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    plants = Plant.objects.filter(countries=country).distinct()

    context = {
        'country': country,
        'plants': plants,
    }
    return render(request, 'plants/country_plants.html', context)
