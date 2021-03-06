from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout, authenticate, login
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, DetailView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

from .forms import RegisterForm, LoginForm, UpdateProfileForm
from .models import Account


# Create your views here.

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "%(username)s glad you joined us!"


class LoginView(SuccessMessageMixin, FormView):
    """
    Login users by email address.
    """
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    success_message = "%(username)s you have been logged in"

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            messages.error(request, "Password or Email incorrect!")
            return super().form_invalid(form)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout.
    """
    url = '/'
    success_message = "%(username)s you have been logged out!"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class UserProfileView(DetailView):
    model = Account
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        user_data = Account.objects.filter(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)

        context['user_data'] = user_data

        return context


class CurrentUserProfileView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Allows users to edit their profiles.
    """
    model = Account
    form_class = UpdateProfileForm
    template_name = 'accounts/edit-profile.html'
    success_url = reverse_lazy('accounts:user-profile')
    success_message = 'Profile updated successfully'

    def get_object(self, queryset=None):
        return self.request.user


class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/delete-profile.html'
    success_url = '/'
    success_message = "%(username)s account has benn deleted!"

    def get_queryset(self):
        return super().get_queryset().filter(username=self.request.user)