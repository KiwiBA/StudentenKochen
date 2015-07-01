import datetime
from django.db import models
from django.utils import timezone
from user_auth.models import Student
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        """
        Returns the the name of ingredient.
        """
        return self.name
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=30)
    
    def __str__(self):
        """
        Returns the the name of tag.
        """
        return self.tagname
    
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipename = models.CharField(max_length=200)
    author = models.ForeignKey(Student, null=True)
    pub_date = models.DateTimeField('date published', editable=False)
    ingredients = models.ManyToManyField(Ingredient, through='Recipeingredients')
    description = models.CharField(max_length=20000)
    tags = models.ManyToManyField(Tag)
    pic = models.ImageField (upload_to="pic_folder/", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        """
        Saves the recipe with current date.
        """
        if not self.id:
            self.pub_date= timezone.now()
        super(Recipe, self).save(*args, **kwargs)
    
    def __str__(self):
        """
        Returns the the name of recipe.
        """
        return self.recipename
    
    # returns true if recipes is published within the last 24 hours.
    def was_published_recently(self):
        """
        Returns the current publish date.
        """
        now = timezone.now()
        return  now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    @models.permalink
    def get_absolute_url(self):
        """
        Returns the absolute url of the recipe.
        """
        return ('recipes:detail', (), {'recipe_id': self.id})

class Recipeingredients(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient)
    recipe = models.ForeignKey(Recipe)
    quantity = models.CharField(max_length=30)
    
    def __str__(self):
        """
        Returns the the string with quantity and ingredient.
        """
        return self.quantity + " " + self.ingredient.name

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe)
    author = models.ForeignKey(Student)
    comment = models.CharField(max_length=2000)
    
    def __str__(self):
        """
        Returns the the the name of the recipe which was commented.
        """
        return "a comment for " + self.recipe.recipename
    
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    evaluator = models.ForeignKey(Student)
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
        """
        Returns the the the name of the recipe which was rated.
        """
        return "a rating for " + self.recipe.recipename