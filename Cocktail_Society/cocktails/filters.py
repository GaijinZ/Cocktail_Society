import django_filters

from .models import Cocktail


class CocktailFilter(django_filters.FilterSet):
    """
    Filter search function by name/ingredient or a category(alcoholic/non-alcoholic).
    """
    class Meta:
        model = Cocktail
        fields = {
            'cocktail_name': ['icontains'],
            'ingredients': ['icontains'],
            'cocktails_category': ['exact']
            }
