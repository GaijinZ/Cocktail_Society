from django.urls import path

from .views import *

app_name = 'cocktails'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('add-cocktail/', AddCocktail.as_view(), name='add-cocktail'),
    path('search-cocktail/', SearchCocktail.as_view(), name='search-cocktail'),
    path('search-ingredients/', SearchIngredients.as_view(), name='search-ingredients'),
    path('search-results/', SearchCocktail.as_view(), name='search-results'),
    path('cocktail-details/<int:pk>/', CocktailDetails.as_view(), name='cocktail-details'),
    path('likes/<int:pk>/', like_view, name='likes'),
]
