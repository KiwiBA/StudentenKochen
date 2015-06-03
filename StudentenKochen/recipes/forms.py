from django.forms import ModelForm
from django import forms
from recipes.models import Recipe, Recipeingredients, Tag

class RecipeForm(forms.ModelForm):
    recipename = forms.CharField(label=(u'Rezeptname'))
    description = forms.CharField(label=(u'Beschreibung'))
    
    tags = forms.CharField(label=(u'Tags'), initial='ToDo: alte Tags anzeigen')
    
    
    
    class Meta:
        model = Recipe
        exclude = ('id', 'author', 'pub_date', 'tags')
       
    def __init__(self, **kwargs):
        self.__user = kwargs.pop('user', None)
        super(RecipeForm, self).__init__(**kwargs)
    
    def save(self, commit=True):
        if self.instance.pk is None:
            if self.__user is None:
                raise TypeError("You didn't give an user argument to the constructor.")
            self.instance.author = self.__user.student
            
            
        self.instance.save()    
        tagList = self.cleaned_data['tags'].split(",")
        existingTags = Tag.objects.all()
        self.instance.tags.through.objects.filter(recipe=self.instance).delete()
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
                self.instance.tags.add(newTag.id)
            else:
                newTag = Tag.objects.filter(tagname=tag)[:1].get()
                self.instance.tags.add(newTag.id)   
        
        
           
        return super(RecipeForm, self).save(commit) 