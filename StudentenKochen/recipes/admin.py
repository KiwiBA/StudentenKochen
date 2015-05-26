from django.contrib import admin
from .models import Tag
from recipes.models import Ingredient
from .models import Recipe
from .models import Recipeingredients
from .models import Comment
from .models import Rating

class IngredientsInline(admin.TabularInline):
    model = Recipeingredients
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    fields = ['recipename', 'author', 'description', 'tags']
    inlines = [IngredientsInline]
    
    list_display = ('id', 'recipename', 'author', 'pub_date')
    list_filter = ['pub_date']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'author')
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'evaluator', 'rating')
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tagname')
    
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')    

admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)