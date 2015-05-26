from django.forms import ModelForm

from recipes.models import Recipe
from django.db.transaction import commit
from user_auth.models import Student

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('id', 'author', 'pub_date')
       
    def __init__(self, **kwargs):
        self.__user = kwargs.pop('user', None)
        super(RecipeForm, self).__init__(**kwargs)
    
    def save(self, commit=True):
        if self.instance.pk is None:
            if self.__user is None:
                raise TypeError("You didn't give an user argument to the constructor.")
            self.instance.author = self.__user.student
            
        return super(RecipeForm, self).save(commit) 