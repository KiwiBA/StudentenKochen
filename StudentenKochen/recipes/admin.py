from django.contrib import admin
from .models import Person
from .models import Tag
from recipes.models import Ingredient
from .models import Recipe
from .models import Recipeingredients
from .models import Comment
from .models import Rating


admin.site.register(Person)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Recipeingredients)
admin.site.register(Comment)
admin.site.register(Rating)