from recipes.models import Recipe, Tag, Recipeingredients, Ingredient
from lib2to3.fixer_util import String
from _overlapped import NULL

def setTags(recipe, tagList):
    
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
#test            
def setRecipeIngredients(request, recipe):
    quantity_str = "quantity"
    ingredient_str = "ingredient"
    
    for x in range(1, 5):
        i= request.POST.get(ingredient_str + str(x)).strip()
        quantity = request.POST.get(quantity_str + str(x)).strip()
        if  quantity and i:
            ri = Recipeingredients()
            existingIngredient = Ingredient.objects.filter(name=i)
            if existingIngredient is not None:
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
                    
    