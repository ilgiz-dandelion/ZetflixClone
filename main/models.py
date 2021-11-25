from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Movie(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='movie')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.comment)

    class Meta:
        ordering = ('-created',)


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.body[:20]}'


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)


class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating) + " | " + self.movie.name + " | " + str(self.user)


class Favorite(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)
