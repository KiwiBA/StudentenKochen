from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from .models import Recipe, Rating, Comment
from recipes.forms import RecipeForm
from recipes.models import Recipeingredients

class IndexView(generic.ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        """Return the last five published recipes."""
        return Recipe.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:20]
    
def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    #compute the rating average of the recipe
    ratings = Rating.objects.all().filter(recipe=recipe)
    all_ratings = 0
    count = 0
    for rating in ratings:
        all_ratings += rating.rating
        count +=1
    if count == 0:
        rating_average = 0
    else:
        rating_average = all_ratings/count
        
    #check if current user rated the recipe already and return the rating the user gave    
    ratingOfCurrentUser = 0
    try:
        userRating = ratings.filter(evaluator=request.user.student)[:1].get()
    except (KeyError, Rating.DoesNotExist):
        ratingOfCurrentUser = 0
    else:
        ratingOfCurrentUser = userRating.rating
    
    #ingredients of the recipe
    recipeIngredients = Recipeingredients.objects.filter(recipe=recipe)
    return render(request, 'recipes/detail.html', {'recipe': recipe, 'ratings': rating_average, 'ratingOfCurrentUser': ratingOfCurrentUser, 'recipeIngredients': recipeIngredients})

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
    if recipe.author != request.user.student and not request.user.is_staff:
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

@login_required     
def rate(request, recipe_id):
    p = get_object_or_404(Recipe, pk=recipe_id)
#     try:

    new_rating = Rating()
    new_rating.recipe = p
    new_rating.evaluator = request.user.student
    new_rating.rating = request.POST['rating']
    new_rating.save()
    return HttpResponseRedirect(p.get_absolute_url())

@login_required    
def comment(request, recipe_id):
    print("COmment")
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user.student
        comment.comment= request.POST.get('comment', '')
        #recipe_id = request.POST.get('recipe_id', '')
        print(recipe_id)
        print("comment" + comment.comment)
        recipe = Recipe.objects.get(id=recipe_id)
        comment.recipe = recipe
        comment.save()
    return HttpResponseRedirect(recipe.get_absolute_url())

def search(request):
    return