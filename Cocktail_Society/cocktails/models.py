from django.db import models
from django.core.exceptions import ValidationError

from datetime import datetime

from accounts.models import Account


# Create your models here.
def validate_image(image):
    file_size = image.file.size
    limit_kb = 150
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


class Cocktail(models.Model):
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
    image = models.ImageField(upload_to='cocktails_pics', validators=[validate_image])
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created = models.DateField(default=datetime.now)
    likes = models.ManyToManyField(Account, default=None, blank=True, related_name='likes')

    objects = models.Manager()

    def __str__(self):
        return f'{self.cocktail_name}, {self.user}'

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    cocktail = models.ForeignKey(Cocktail, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.cocktail}, {self.name}'
