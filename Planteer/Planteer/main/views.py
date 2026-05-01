from django.shortcuts import render
from plants.models import Plant,Comment, Country


def home_view(request):

    if request.user.is_authenticated:
        print(request.user.email)
    else:
        print("User is not logged in")


    plants = Plant.objects.all().order_by('-created_at')[:8]
    return render(request, 'main/home.html', {
        'plants': plants,
         'plants_count': Plant.objects.count(),
        'comments_count': Comment.objects.count(),
        'countries_count': Country.objects.count(),})
