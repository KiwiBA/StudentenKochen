import datetime

from django.db import models
from django.utils import timezone

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    receptname = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    ingredients = models.ManyToManyField(Ingredient, through='Recipeingredients')
    description = models.CharField(max_length=20000)
    
    def __str__(self):
        return self.receptname
    
    # returns true if recipes is published within the last 24 hours.
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Recipeingredients(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient)
    recipe = models.ForeignKey(Recipe)
    quantity = models.CharField(max_length=30)
    
    def __str__(self):
        return self.ingredient + " is ingredient of " + self.recipe

