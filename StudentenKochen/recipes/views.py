from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.db.models import Q #for complex queries
import re #regular expressions


from .models import Recipe, Rating, Comment, Tag
from recipes.models import Recipeingredients
from _overlapped import NULL
from .helperfunctions import *

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
    ratingOfCurrentUser = NULL
    for rating in ratings:
        all_ratings += rating.rating
        count +=1
    if count == 0:
        rating_average = 0
    else:
        rating_average = all_ratings/count
        
    if request.user.is_authenticated(): 
        #check if current user rated the recipe already and return the rating the user gave    
        try:
            userRating = ratings.filter(evaluator=request.user.student)[:1].get()
        except (KeyError, Rating.DoesNotExist):
            ratingOfCurrentUser = 0
        else:
            ratingOfCurrentUser = userRating.rating
    #get all comments of current recipe
    comments = Comment.objects.filter(recipe=recipe)
    #ingredients of the recipe
    recipeIngredients = Recipeingredients.objects.filter(recipe=recipe)
    
    return render(request, 'recipes/detail.html', {'recipe': recipe, 'ratings': rating_average, 'ratingOfCurrentUser': ratingOfCurrentUser, 'recipeIngredients': recipeIngredients, 'comments':comments})

@login_required
def create(request):
    if request.method == 'POST':
        recipe = Recipe()
        recipe.recipename = request.POST.get('recipename')
        
        recipe.author = request.user.student
        recipe.description = request.POST.get('description')
        recipe.save()
        setRecipeIngredients(request, recipe)
        
        setTags(recipe, request.POST.get('tag').split(","))
        recipe.save()
        return HttpResponseRedirect(recipe.get_absolute_url())
    return render(request, 'recipes/create.html')

@login_required
def edit(request, recipe_id):
   pass

@login_required     
def rate(request, recipe_id):
    p = get_object_or_404(Recipe, pk=recipe_id)
    new_rating = Rating()
    new_rating.recipe = p
    new_rating.evaluator = request.user.student
    new_rating.rating = request.POST['rating']
    new_rating.save()
    
    return HttpResponseRedirect(p.get_absolute_url())

@login_required    
def comment(request, recipe_id):
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user.student
        comment.comment= request.POST.get('comment', '')
        recipe = Recipe.objects.get(id=recipe_id)
        comment.recipe = recipe
        comment.save()
        
    return HttpResponseRedirect(recipe.get_absolute_url())

def ownRecipes(request):
    author = request.user.student
    print(author.name)
    recipes= Recipe.objects.filter(author=author)
    
    return render(request, 'recipes/ownRecipe.html', {'recipe_list': recipes})

def extendedSearch(request):
    query_string_title = None
    query_string_ingredient = None
    query_string_tag = None 
    query_string_author = None
    found_entries = None
    query_string = ''
    
    if ('title' in request.GET) or ('ingredient' in request.GET) or ('tag' in request.GET) or ('author' in request.GET):
        query_string_title = request.GET['title']
        query_string_ingredient = request.GET['ingredient']
        query_string_tag = request.GET['tag']
        query_string_author = request.GET['author']
        query_string = query_string_title + " " + query_string_ingredient + " " + query_string_tag + " " + query_string_author
        print(query_string_title + query_string_ingredient+query_string_tag+query_string_author)
        unordered_query = make_extended_query(query_string_title, query_string_ingredient, query_string_tag, query_string_author)
        print(unordered_query)     
        found_entries = unordered_query.order_by('-pub_date')
        print(found_entries)
    if query_string_title==None and query_string_ingredient ==None and query_string_tag == None and query_string_author ==None:    
        return render(request, 'recipes/extendedSearch.html')
    else:
        return render(request, 'recipes/search.html', { 'query_string':query_string,  'found_entries': found_entries})
#     return render_to_response('recipes/extendedSearch.html',
#                           { 'query_string': query_string, 'found_entries': found_entries },
#                           context_instance=RequestContext(request))

    
    #return HttpResponseRedirect('recipes/search.html', { 'query_string': query_string, 'found_entries': found_entries })

def search(request):
    query_string = ''
    found_entries = None
    
    
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        unordered_query = make_query(query_string, ['recipename', 'description', 'tags.tagname', 'ingredients.name'])    
        print(unordered_query)     
        found_entries = Recipe.objects.filter(unordered_query).order_by('-pub_date')

    return render(request, 'recipes/search.html', {'query_string': query_string, 'found_entries': found_entries})
    
def make_query(query_string, search_fields):
    #regular expressions um die suchwoerter zu trennen
    findterms = re.compile(r'"([^"]+)"|(\S+)').findall
    normspace=re.compile(r'\s{2,}').sub
    terms = [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
    
    query = None # Query to search for every search term 
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            field_name = field_name.replace(".", "__") #ersetze den punkt mit __ um auch in fremdschluesseln zu suchen
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def make_extended_query(query_string_title, query_string_ingredient, query_string_tag, query_string_author):
    q = None
    q = Recipe.objects.filter(recipename__icontains=query_string_title, tags__tagname__icontains= query_string_tag, 
           ingredients__name__icontains= query_string_ingredient, author__name__icontains= query_string_author).distinct()
    return q