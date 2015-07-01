# -*- coding: iso-8859-1 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
import logging
from .models import Recipe, Rating, Comment, Tag
from recipes.models import Recipeingredients
from _overlapped import NULL
from .helperfunctions import *

recipe_logger = logging.getLogger('recipes')
    
def detail(request, recipe_id):
    """
    Detail View for current recipe.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
        
    rating_average, ratingOfCurrentUser = computeRatings(request, recipe)
    #comments of current recipe
    comments = Comment.objects.filter(recipe=recipe)
    #ingredients of current recipe
    recipeIngredients = Recipeingredients.objects.filter(recipe=recipe)
    
    return render(request, 'recipes/detail.html', {'recipe': recipe, 
                                                   'ratings': rating_average, 
                                                   'ratingOfCurrentUser': ratingOfCurrentUser, 
                                                   'recipeIngredients': recipeIngredients, 
                                                   'comments':comments})
    
@login_required
def create(request):
    """
    Creates a new recipe objects and saves in db.
    """
    if request.method == 'POST':
        recipe = Recipe()
        recipe.recipename = request.POST.get('recipename')
        recipe.author = request.user.student
        recipe.description = request.POST.get('description')
        recipe.save()
        
        setRecipeIngredients(request, recipe)
        setTags(recipe, request.POST.get('tag').split(","))
       
        recipe_logger.info("Recipe %s was created successfully", recipe.recipename)
        if 'pic' in request.FILES:
            recipe.pic = request.FILES['pic']
        recipe.save()
        return HttpResponseRedirect(recipe.get_absolute_url())
    
    return render(request, 'recipes/create.html')

@login_required
def edit(request, recipe_id):
    """
    User can edit his own recipe.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_logger.info("EditView was called for recipe %s", recipe.recipename)
    
    if recipe.author != request.user.student:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        recipe.recipename = request.POST.get('recipename')
        recipe.description = request.POST.get('description')
        setTags(recipe, request.POST.get('tag').split(","))
        editRecipeIngredients(request, recipe)
        if 'edit_pic' in request.FILES:
            recipe.pic = request.FILES['edit_pic']
        recipe.save()
        recipe_logger.info("Recipe %s was edited successfully", recipe.recipename)
        return HttpResponseRedirect(recipe.get_absolute_url())
    
    recipeTags = getTags(recipe)
    recipeIngredients = Recipeingredients.objects.filter(recipe=recipe)
    
    return render(request, 'recipes/edit.html', {'recipe': recipe, 
                                                 'recipeIngredients': recipeIngredients, 
                                                 'recipeTags':recipeTags})

@login_required
def delete(request, recipe_id):
    """
    Deletes the current recipe of the owner.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if recipe.author != request.user.student and not request.user.is_staff:
        return HttpResponseForbidden()
    else:
        
        m = u"Rezept ''" + recipe.recipename + "'' gelöscht."
        messages.add_message(request, messages.SUCCESS, m)
        recipe.delete()
        recipe_logger.info("Recipe %s was deleted successfully", recipe.recipename)
       
        
    author = request.user.student
    recipes= Recipe.objects.filter(author=author)
    
    return render(request, 'recipes/ownRecipe.html', {'recipe_list': recipes})
    
@login_required     
def rate(request, recipe_id):
    """
    Saves the rating of the current user for the current recipe.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    new_rating = Rating()
    new_rating.recipe = recipe
    new_rating.evaluator = request.user.student
    new_rating.rating = request.POST['rating']
    new_rating.save()
    
    recipe_logger.info("Rating for recipe %s was created succesfully", recipe.recipename)
    return HttpResponseRedirect(recipe.get_absolute_url())

@login_required    
def comment(request, recipe_id):
    """
    Saves the current user comment for the current recipe.
    """
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user.student
        comment.comment= request.POST.get('comment', '')
        recipe = Recipe.objects.get(id=recipe_id)
        comment.recipe = recipe
        comment.save()
        recipe_logger.info("A new comment for recipe %s was commented", recipe.recipename)
    
    return HttpResponseRedirect(recipe.get_absolute_url())

@login_required 
def ownRecipes(request):
    """
    Lists the own recipes of current user.
    """
    author = request.user.student
    recipes= Recipe.objects.filter(author=author)
    
    return render(request, 'recipes/ownRecipe.html', {'recipe_list': recipes})

def extendedSearch(request):
    """
    Returns a list of the the current extended search.
    """
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
        
        unordered_query = make_extended_query(query_string_title,
                                               query_string_ingredient, 
                                               query_string_tag, 
                                               query_string_author)
         
        found_entries = unordered_query.order_by('-pub_date')
     
    if query_string_title==None and query_string_ingredient ==None and query_string_tag == None and query_string_author ==None:    
        return render(request, 'recipes/extendedSearch.html')
    else:
        return render(request, 'recipes/search.html', { 'query_string':query_string, 
                                                        'found_entries': found_entries})

def search(request):
    """
    Returns a list of the the current search.
    """
    query_string = ""
    found_entries = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        unordered_query = make_query(query_string, ['recipename', 'description',
                                                     'tags.tagname', 'ingredients.name'])        
        found_entries = Recipe.objects.filter(unordered_query).order_by('-pub_date')

    return render(request, 'recipes/search.html', {'query_string': query_string, 
                                                   'found_entries': found_entries})
    
