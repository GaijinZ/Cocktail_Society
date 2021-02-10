from django import forms

from .models import Cocktail, Comment


class AddCocktailForm(forms.ModelForm):
    ingredients = forms.CharField(max_length=100,
                                  widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))
    execution = forms.CharField(max_length=150,
                                widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        object = super().save(commit=False)
        object.user = self.request.user
        object.save()
        return object

    class Meta:
        model = Cocktail
        fields = ['cocktail_name',
                  'cocktails_category',
                  'crockery_category',
                  'method_category',
                  'ingredients',
                  'execution',
                  'image',
                  ]


class CommentForm(forms.ModelForm):
    body = forms.CharField(max_length=150,
                           widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))

    class Meta:
        model = Comment
        fields = ['body']
