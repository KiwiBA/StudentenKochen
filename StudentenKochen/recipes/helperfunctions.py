from recipes.models import Recipe, Tag, Recipeingredients, Ingredient, Rating
from lib2to3.fixer_util import String
from _overlapped import NULL
from django.db.models import Q #for complex queries
import re #regular expressions

def computeRatings(request, recipe):
    """
    Computes the rating average of the recipe.
    """
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
            
    return rating_average, ratingOfCurrentUser

def setTags(recipe, tagList):
    """
    saves the Tags in Recipe object.
    """
    existingTags = Tag.objects.all()
    recipe.tags.through.objects.filter(recipe=recipe).delete()
        
    for tag in tagList:
        tag.strip()
        is_existing = False
        for existingTag in existingTags:
            if tag.lower() == existingTag.tagname.lower():
                is_existing = True
        
        newTag = Tag()
        newTag.tagname = tag
        if is_existing == False:
            newTag.save()
            newTag = Tag.objects.filter(tagname=tag)[:1].get()
            recipe.tags.add(newTag.id)
        else:
            newTag = Tag.objects.filter(tagname=tag)[:1].get()
            recipe.tags.add(newTag.id)
            
def setRecipeIngredients(request, recipe):
    """
    Saves the current ingredients and quantity for Recipe.
    """
    quantity_str = "quantity"
    ingredient_str = "ingredient"
    
    for x in range(1, 5):
        i= request.POST.get(ingredient_str + str(x)).strip()
        quantity = request.POST.get(quantity_str + str(x)).strip()
        if  quantity and i:
            ri = Recipeingredients()
            existingIngredient = None
            existingIngredient = Ingredient.objects.filter(name=i)
            if not len(existingIngredient) == 0 :
                for ingredient in existingIngredient:
                    ri.ingredient = ingredient
                    ri.recipe = recipe
                    ri.quantity = quantity
                    ri.save()
                    
            else:
                ingredient = Ingredient()
                ingredient.name = i
                ingredient.save()
                ri.ingredient = ingredient
                ri.recipe = recipe
                ri.quantity = quantity
                ri.save()
                
def editRecipeIngredients(request, recipe):
    """
    Saves the current RecipeIngredients objects for the current recipe.
    """
    recipeIngredients = Recipeingredients.objects.filter(recipe=recipe)
    quantity_str = "quantity"
    ingredient_str = "ingredient"
    
    for x in recipeIngredients:
        i= request.POST.get(ingredient_str + str(x.id)).strip()
        quantity = request.POST.get(quantity_str + str(x.id)).strip()
        if  quantity and i:
            existingIngredient = Ingredient.objects.filter(name=i)
            if not len(existingIngredient) == 0:
                for ingredient in existingIngredient:
                    x.ingredient = ingredient
                    x.quantity = quantity
            else:
                ingredient = Ingredient()
                ingredient.name = i
                ingredient.save()
                x.ingredient = ingredient
                x.quantity = quantity
            x.save()
            
def getTags(recipe):
    """
    Returns the tags in a string.
    """
    tags = Tag.objects.filter(recipe=recipe)
    tag_str = ""
    for tag in tags:
        tag_str += tag.tagname + ", " 
    
    return tag_str[:-2] 
    
     
def make_query(query_string, search_fields):
    """
    Creates a query for recipe search.
    """
    findterms = re.compile(r'"([^"]+)"|(\S+)').findall
    normspace=re.compile(r'\s{2,}').sub
    terms = [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
    
    query = None
    for term in terms:
        or_query = None 
        for field_name in search_fields:
            field_name = field_name.replace(".", "__")
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
    """
    Makes an extended query for Recipe.
    """
    q = None
    q = Recipe.objects.filter(recipename__icontains =
                              query_string_title, 
                              tags__tagname__icontains = 
                              query_string_tag, 
                              ingredients__name__icontains =
                              query_string_ingredient, 
                              author__name__icontains = 
                              query_string_author).distinct()
    return q   