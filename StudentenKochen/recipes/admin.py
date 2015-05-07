from django.contrib import admin
from .models import Person
from .models import Tag
from recipes.models import Ingredient
from .models import Recipe
from .models import Recipeingredients
from .models import Comment
from .models import Rating

class IngredientsInline(admin.StackedInline):
    model = Recipeingredients
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    fields = ['recipename', 'author', 'pub_date', 'description', 'tags']
    inlines = [IngredientsInline]

admin.site.register(Person)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)
admin.site.register(Rating)