from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from .models import Recipe, Rating

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

def create(request):
    return render(request, 'recipes/create.html')