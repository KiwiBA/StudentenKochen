# -*- coding: utf8 -*-
from django.shortcuts import render
from recipes.models import Recipe
from django.utils import timezone

def index(request):
    """
    Lists the 20 up to date recipes ordered by pub_date.
    """
    recipe_list = Recipe.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:20]
    
    return render(request, 'home/index.html', {'recipe_list': recipe_list})