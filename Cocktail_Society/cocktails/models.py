from django.db import models
from datetime import datetime

from accounts.models import Account


# Create your models here.
class AddCocktails(models.Model):
    COCKTAIL_CATEGORY = (
        ('alc', 'Alcoholic'),
        ('nonalc', 'Noc-Alcoholic')
    )
    GLASS_CATEGORY = (
        ('short', 'Short'),
        ('long', 'Long')
    )
    METHODS = (
        ('stir', 'Stirren'),
        ('shake', 'Shaken'),
        ('build', 'Build')
    )

    cocktail_name = models.CharField(max_length=100, null=True)
    cocktails_category = models.CharField(max_length=50, choices=COCKTAIL_CATEGORY)
    crockery_category = models.CharField(max_length=50, choices=GLASS_CATEGORY)
    method_category = models.CharField(max_length=50, choices=METHODS)
    ingredients = models.TextField(max_length=100, null=True)
    execution = models.TextField(max_length=150)
    image = models.ImageField(upload_to='cocktails_pics')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.now)
    likes = models.ManyToManyField(Account, default=None, blank=True, related_name='likes')

    objects = models.Manager()

    def __str__(self):
        return f'{self.cocktail_name}, {self.user}'

    def total_likes(self):
        return self.likes.count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    cocktail = models.ForeignKey(AddCocktails, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return self.cocktail
