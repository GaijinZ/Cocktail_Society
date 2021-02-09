from django.contrib import admin

from .models import Cocktail, Comment
# Register your models here.

admin.site.register(Cocktail)
admin.site.register(Comment)

