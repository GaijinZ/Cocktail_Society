from django.urls import path

from .views import *

app_name = 'cocktails'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('add-cocktail/', AddCocktail.as_view(), name='add-cocktail'),
    path('search-cocktail/', SearchCocktail.as_view(), name='search-cocktail'),
    path('search-ingredients/', SearchIngredients.as_view(), name='search-ingredients'),
    path('search-results/', SearchCocktail.as_view(), name='search-results')
]
