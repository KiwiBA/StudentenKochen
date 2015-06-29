from django.shortcuts import render
from recipes.models import Recipe
from django.utils import timezone

def index(request):
    recipe_list = Recipe.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:20]
    return render(request, 'home/index.html', {'recipe_list': recipe_list})