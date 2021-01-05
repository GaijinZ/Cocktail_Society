import django_filters

from .models import AddCocktails


class CocktailFilter(django_filters.FilterSet):

    class Meta:
        model = AddCocktails
        fields = {
            'cocktail_name': ['icontains'],
            'ingredients': ['icontains'],
            'cocktails_category': ['exact']
            }
