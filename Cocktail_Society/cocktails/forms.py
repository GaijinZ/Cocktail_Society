from django import forms

from .models import AddCocktails


class AddCocktailForm(forms.ModelForm):
    ingredients = forms.CharField(max_length=100,
                                  widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))
    execution = forms.CharField(max_length=150,
                                widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))

    class Meta:
        model = AddCocktails
        fields = ['cocktail_name',
                  'cocktails_category',
                  'crockery_category',
                  'method_category',
                  'ingredients',
                  'execution',
                  'image',
                  ]
