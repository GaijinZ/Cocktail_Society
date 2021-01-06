from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse

from django_filters.views import FilterView

from .forms import AddCocktailForm
from .models import AddCocktails
from .filters import CocktailFilter


# Create your views here.
def like_view(request, pk):
    cocktail = get_object_or_404(AddCocktails, id=pk)
    liked = False
    if cocktail.likes.filter(id=request.user.id).exists():
        cocktail.likes.remove(request.user)
        liked = False
    else:
        cocktail.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('cocktails:cocktail-details', args=[str(pk)]))


class HomePageView(ListView):
    template_name = 'cocktails/home.html'
    model = AddCocktails

    def get_queryset(self):
        return AddCocktails.objects.annotate(total_likes=Count('likes')).filter(total_likes__gt=0).order_by('-date')[:5]


class AboutPageView(TemplateView):
    template_name = 'cocktails/about.html'


class AddCocktail(SuccessMessageMixin, LoginRequiredMixin, FormView):
    model = AddCocktails
    form_class = AddCocktailForm
    template_name = 'cocktails/add-cocktail.html'
    success_url = '/'
    success_message = 'Cocktail added'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class SearchCocktail(LoginRequiredMixin, FilterView):
    template_name = 'cocktails/search-cocktail.html'
    model = AddCocktails
    context_object_name = 'cocktail_list'
    filterset_class = CocktailFilter


class CocktailDetails(LoginRequiredMixin, DetailView):
    model = AddCocktails
    template_name = 'cocktails/cocktail-details.html'

    def get_context_data(self, *args, **kwargs):
        cocktail_data = AddCocktails.objects.filter(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(AddCocktails, id=self.kwargs['pk'])
        total_likes = stuff.total_likes

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['cocktail_data'] = cocktail_data
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class SearchIngredients(LoginRequiredMixin, TemplateView):
    template_name = 'cocktails/search-ingredients.html'

