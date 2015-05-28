from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from .models import Recipe, Rating, Comment
from recipes.forms import RecipeForm

class IndexView(generic.ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        """Return the last five published recipes."""
        return Recipe.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
# def index(request):
#     latest_recipe_list = Recipe.objects.order_by('-pub_date')[:2]
#     template = loader.get_template('recipes/index.html')
#     context = RequestContext(request, {
#         'latest_recipe_list': latest_recipe_list,
#     })
#     return HttpResponse(template.render(context))

# class DetailView(generic.DetailView):
#     model = Recipe
#     template_name = 'recipes/detail.html'
    
def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ratings = Rating.objects.all().filter(recipe=recipe)
    all_ratings = 0
    count = 0
    for rating in ratings:
        all_ratings += rating.rating
        count +=1
    if count == 0:
        rating_average = 0
    else:
        rating_average = all_ratings/count
    return render(request, 'recipes/detail.html', {'recipe': recipe, 'ratings': rating_average})

@login_required
def create(request):
    if request.method == 'POST':
        form = RecipeForm(user=request.user, data=request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render(request, 'recipes/create.html',
        {'form': form, 'add': True})

@login_required
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user.student and not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = RecipeForm(instance=recipe, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/create.html',
        {'form': form, 'add': False, 'object': recipe})

@login_required     
def rate(request, recipe_id):
    p = get_object_or_404(Recipe, pk=recipe_id)
#     try:
    new_rating = Rating()
    new_rating.recipe = p
    new_rating.evaluator = request.user.student
    new_rating.rating = request.POST['rating']
    new_rating.save()
#         selected_choice = p.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': p,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
    return HttpResponseRedirect(p.get_absolute_url())

@login_required    
def comment(request, recipe_id):
    print("COmment")
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user.student
        comment.comment= request.POST.get('comment', '')
        #recipe_id = request.POST.get('recipe_id', '')
        print(recipe_id)
        print("comment" + comment.comment)
        recipe = Recipe.objects.get(id=recipe_id)
        comment.recipe = recipe
        comment.save()
    return HttpResponseRedirect(recipe.get_absolute_url())