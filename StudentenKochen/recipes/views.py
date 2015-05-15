from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render

from .models import Recipe

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:2]
    template = loader.get_template('recipes/index.html')
    context = RequestContext(request, {
        'latest_recipe_list': latest_recipe_list,
    })
    return HttpResponse(template.render(context))

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipename = recipe.recipename
    return render(request, 'recipes/detail.html', {'recipe': recipe})