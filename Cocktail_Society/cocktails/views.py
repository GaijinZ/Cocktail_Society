from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django_filters.views import FilterView

from .forms import AddCocktailForm
from .models import AddCocktails
from .filters import CocktailFilter


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'cocktails/home.html'


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


class SearchIngredients(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cocktails/search-ingredients.html')
