import self as self
from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    author = models.CharField(max_length=50)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',
    )
    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers', blank=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(News, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class CategorySubscribers(models.Model):
    subscriber_thru = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category_thru = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
