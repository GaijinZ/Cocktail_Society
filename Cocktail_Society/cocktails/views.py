from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DetailView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django_filters.views import FilterView

from .forms import AddCocktailForm, CommentForm
from .models import Cocktail, Comment
from .filters import CocktailFilter


# Create your views here.
def like_view(request, pk):
    """
    Like/Unlike system, if it is already liked - Unlike button shows.
    """
    cocktail = get_object_or_404(Cocktail, id=pk)
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
    model = Cocktail

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        most_likes = Cocktail.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:5]
        recently_added = Cocktail.objects.all().order_by('-created')[:5]
        recently_commented = Comment.objects.all().order_by('-date_added')[:5]

        context['most_likes'] = most_likes
        context['recently_added'] = recently_added
        context['recently_commented'] = recently_commented
        return context


class AddCocktail(SuccessMessageMixin, LoginRequiredMixin, FormView):
    """
    Page to add your cocktail with all the description and image.
    """
    model = Cocktail
    form_class = AddCocktailForm
    template_name = 'cocktails/add-cocktail.html'
    success_url = '/'
    success_message = 'Cocktail added'


class SearchCocktail(LoginRequiredMixin, FilterView):
    """
    Search for cocktails system, can search by name, by category - alcoholic/non-alcoholic,
    by ingredient it contains.
    """
    template_name = 'cocktails/search-cocktail.html'
    model = Cocktail
    filterset_class = CocktailFilter
    success_url = 'cocktails/search-results.html'


class SearchResults(LoginRequiredMixin, FilterView):
    """
    All the results from SearchCocktail class are showing in here.
    """
    template_name = 'cocktails/search-results.html'
    model = Cocktail
    context_object_name = 'cocktail_list'
    filterset_class = CocktailFilter
    paginate_by = 10


class CocktailDetails(DetailView):
    """
    View for a cocktail details page, shows author, name, category, type of glass,
    method to make, ingredient needed to make one, description and a picture.
    """
    model = Cocktail
    template_name = 'cocktails/cocktail-details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        cocktail_data = Cocktail.objects.filter(id=self.kwargs['pk'])
        stuff = get_object_or_404(Cocktail, id=self.kwargs['pk'])
        total_likes = stuff.total_likes

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['cocktail_data'] = cocktail_data
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class MyCocktailList(ListView):
    """
    List of cocktails made by logged/selected user.
    """
    model = Cocktail
    template_name = 'cocktails/my-cocktails.html'
    context_object_name = 'cocktail_list'
    paginate_by = 10

    def get_queryset(self):
        return Cocktail.objects.filter(user=self.kwargs['pk'])


class DeleteCocktail(LoginRequiredMixin, DeleteView):
    """
    Delete cocktail page
    """
    model = Cocktail
    template_name = 'cocktails/delete-cocktail.html'
    success_url = reverse_lazy('cocktails:home')
    success_message = 'Cocktail deleted successfully'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'cocktails/add-comment.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.cocktail_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)
