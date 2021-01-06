from django.contrib import admin

from .models import AddCocktails, Like
# Register your models here.

admin.site.register(AddCocktails)
admin.site.register(Like)
