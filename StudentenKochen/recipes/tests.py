from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Recipe

class RecipeMethodTests(TestCase):
    
    def test_was_published_recently_with_future_recipe(self):
        """
        was_published_recently() should return False for recipes whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_recipe = Recipe(pub_date=time)
        self.assertEqual(future_recipe.was_published_recently(), False)
        
    def test_was_published_recently_with_old_recipe(self):
        """
        was_published_recently() should return False for recipes whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_recipe = Recipe(pub_date=time)
        self.assertEqual(old_recipe.was_published_recently(), False)

    def test_was_published_recently_with_recent_recipe(self):
        """
        was_published_recently() should return True for recipes whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_recipe = Recipe(pub_date=time)
        self.assertEqual(recent_recipe.was_published_recently(), True)