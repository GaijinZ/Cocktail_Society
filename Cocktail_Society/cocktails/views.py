from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django_filters.views import FilterView

from .forms import AddCocktailForm
from .models import AddCocktails
from .filters import CocktailFilter


# Create your views here.
def like_view(request, pk):
    """
    Like/Unlike system, if it is already liked - Unlike button shows.
    """
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
    """
    Home page with top 5 cocktails with most likes.
    """
    template_name = 'cocktails/home.html'
    model = AddCocktails

    def get_queryset(self):
        return AddCocktails.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:5]


class AboutPageView(TemplateView):
    template_name = 'cocktails/about.html'


class AddCocktail(SuccessMessageMixin, LoginRequiredMixin, FormView):
    """
    Page to add your cocktail with all the description and image.
    """
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
    """
    Search for cocktails system, can search by name, by category - alcoholic/non-alcoholic,
    by ingredient it contains.
    """
    template_name = 'cocktails/search-cocktail.html'
    model = AddCocktails
    filterset_class = CocktailFilter
    success_url = 'cocktails/search-results.html'


class SearchResults(LoginRequiredMixin, FilterView):
    """
    All the results from SearchCocktail class are showing in here.
    """
    template_name = 'cocktails/search-results.html'
    model = AddCocktails
    context_object_name = 'cocktail_list'
    filterset_class = CocktailFilter
    paginate_by = 10


class CocktailDetails(DetailView):
    """
    View for a cocktail details page, shows author, name, category, type of glass,
    method to make, ingredient needed to make one, description and a picture.
    """
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


class MyCocktailList(ListView):
    """
    List of cocktails made by logged/selected user.
    """
    model = AddCocktails
    template_name = 'cocktails/my-cocktails.html'
    context_object_name = 'cocktail_list'
    paginate_by = 10

    def get_queryset(self):
        return AddCocktails.objects.filter(user=self.kwargs['pk'])


class DeleteCocktail(LoginRequiredMixin, DeleteView):
    """
    Delete cocktail page
    """
    model = AddCocktails
    template_name = 'cocktails/delete-cocktail.html'
    success_url = reverse_lazy('cocktails:home')
    success_message = 'Cocktail deleted successfully'

    # Test user permission
    def test_func(self):
        cocktail = self.get_object()
        if self.request.user == cocktail.account.username:
            return True
        return False
