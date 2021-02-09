from django import forms

from .models import Cocktail, Comment


class AddCocktailForm(forms.ModelForm):
    ingredients = forms.CharField(max_length=100,
                                  widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))
    execution = forms.CharField(max_length=150,
                                widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))

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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        object = super().save(commit=False)
        object.user = self.request.user
        object.save()
        return object


class CommentForm(forms.ModelForm):
    body = forms.CharField(max_length=150,
                           widget=forms.Textarea(attrs={'rows': '4', 'cols': '40'}))

    class Meta:
        model = Comment
        fields = ['body']
