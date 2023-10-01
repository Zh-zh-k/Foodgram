from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Recipe, User, Follow
from .forms import RecipeForm
from .utils import pages


def index(request):
    template = 'recipes/index.html'
    recipes = Recipe.objects.order_by('-pub_date')
    page_obj = pages(request, recipes)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'recipes/profile.html'
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.all()
    page_obj = pages(request, recipes)
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user,
                                          author=author).exists()
    else:
        following = False
    context = {
        'page_obj': page_obj,
        'author': author,
        'following': following
    }
    return render(request, template, context)


def recipe_detail(request, recipe_name):
    template = 'recipes/recipe_detail.html'
    recipe = get_object_or_404(Recipe, name=recipe_name)
    context = {
        'recipe': recipe
    }
    return render(request, template, context)


@login_required
def recipe_create(request):
    template = 'recipes/create_recipe.html'
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('recipes:profile', username=request.user)
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    context = {
        'title': 'Новый рецепт',
        'form': form,
    }
    return render(request, template, context)


@login_required
def recipe_edit(request, recipe_name):
    template = 'recipes/create_recipe.html'
    recipe = get_object_or_404(Recipe, name=recipe_name)
    if request.user == recipe.author:
        if request.method == 'POST':
            form = RecipeForm(request.POST or None,
                              files=request.FILES or None,
                              instance=recipe)
            if form.is_valid():
                form.save()
                return redirect('recipes:recipe_detail', recipe_name)
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe)
        context = {
            'title': 'Редактировать рецепт',
            'form': form,
            'is_edit': True,
            'recipe': recipe
        }
        return render(request, template, context)
    else:
        return redirect('recipes:recipe_detail', recipe_name)


@login_required
def follow_index(request):
    template = 'recipes/follow.html'
    recipes = Recipe.objects.filter(author__following__user=request.user,)
    page_obj = pages(request, recipes)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    if user == author:
        return redirect('recipes:profile', username=username)
    Follow.objects.get_or_create(author=author, user=request.user)
    return redirect('recipes:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('recipes:profile', username=username)
