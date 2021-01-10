from django.urls import path

from .views import *
from . import views

app_name = 'cocktails'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('add-cocktail/', AddCocktail.as_view(), name='add-cocktail'),
    path('search-cocktail/', SearchCocktail.as_view(), name='search-cocktail'),
    path('search-ingredients/', SearchIngredients.as_view(), name='search-ingredients'),
    path('search-results/', SearchResults.as_view(), name='search-results'),
    path('cocktail-details/<int:pk>/', CocktailDetails.as_view(), name='cocktail-details'),
    path('likes/<int:pk>/', views.like_view, name='likes'),
    path('my-cocktails/<int:pk>', MyCocktailList.as_view(), name='my-cocktails'),
    path('cocktail-details/<int:pk>/delete', DeleteCocktail.as_view(), name='delete-cocktail'),
]
