from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from .models import Recipe, Rating
from recipes.forms import RecipeForm

class IndexView(generic.ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        """Return the last five published recipes."""
        return Recipe.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
# def index(request):
#     latest_recipe_list = Recipe.objects.order_by('-pub_date')[:2]
#     template = loader.get_template('recipes/index.html')
#     context = RequestContext(request, {
#         'latest_recipe_list': latest_recipe_list,
#     })
#     return HttpResponse(template.render(context))

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'

# def detail(request, recipe_id):
#     recipe = get_object_or_404(Recipe, pk=recipe_id)
#     recipename = recipe.recipename
#     return render(request, 'recipes/detail.html', {'recipe': recipe})

@login_required
def create(request):
    if request.method == 'POST':
        form = RecipeForm(user=request.user, data=request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render(request, 'recipes/create.html',
        {'form': form, 'add': True})

@login_required
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = RecipeForm(instance=recipe, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/create.html',
        {'form': form, 'add': False, 'object': recipe})