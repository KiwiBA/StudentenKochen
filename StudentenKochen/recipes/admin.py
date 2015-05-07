from django.contrib import admin
from recipes.models import Ingredient
from .models import Recipe
from .models import Recipeingredients


admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Recipeingredients)