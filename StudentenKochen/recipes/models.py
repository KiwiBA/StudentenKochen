import datetime

from django.db import models
from django.utils import timezone

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    username = models.CharField(max_length=200)
    pw = models.CharField(max_length=200)
    
    def __str__(self):
        return self.email + " --- " + self.username

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=30)
    
    def __str__(self):
        return self.tagname
    
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipename = models.CharField(max_length=200)
    author = models.ForeignKey(Person, null=True)
    pub_date = models.DateTimeField('date published')
    ingredients = models.ManyToManyField(Ingredient, through='Recipeingredients')
    description = models.CharField(max_length=20000)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.recipename
    
    # returns true if recipes is published within the last 24 hours.
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Recipeingredients(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient)
    recipe = models.ForeignKey(Recipe)
    quantity = models.CharField(max_length=30)
    
    def __str__(self):
        return self.ingredient.name + " is ingredient of " + self.recipe.recipename

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe)
    author = models.ForeignKey(Person)
    comment = models.CharField(max_length=2000)
    
    def __str__(self):
        return "a comment for " + self.recipe.recipename
    
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    evaluator = models.ForeignKey(Person)
    recipe = models.ForeignKey(Recipe)
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),              
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=3)
    
    def __str__(self):
        return "a rating for " + self.recipe.recipename