
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpRequest,HttpResponse
from .models import Plant,Commint
from .forms import PlantForm


def all_plants_view(request):
    plants = Plant.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category:
        plants = plants.filter(category=category)

    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.Category.choices
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

def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    comments = Commint.objects.filter(plant=plant)

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments
    })