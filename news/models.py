from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
# Модель содержит основные поля и поведение данных. Одна модель представляет одну таблицу в БД


# Класс модели может содержать разные аргументы
class Author(models.Model):
    # поля модели, указываются как атрибут класса и каждый атрибут соответствует полю таблицы в БД
    user = models.OneToOneField(User, on_delete=models.CASCADE) # содержит аргументы полей модели
    rating = models.IntegerField(default=0)

    def update_rating(self):
        article_rating = Post.objects.filter(news_or_article="2", author=self.id).values('rating')
        sum_rating_of_article = 0
        for r in article_rating:
            sum_rating_of_article += (r['rating'] * 3)
        sum_rating_comment = 0
        news_rating = Post.objects.filter(news_or_article="1", author=self.id).values('rating')
        sum_rating_of_news = 0
        for n in news_rating:
            sum_rating_of_news += n['rating']
        comment_rating = Comment.objects.filter(user=self.id).values('rating')
        for c in comment_rating:
            sum_rating_comment += c['rating']
        self.rating = sum_rating_of_article + sum_rating_of_news + sum_rating_comment
        self.save()
        return self.rating
    # методы модели работают с конкретной записью в таблице

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribers')


    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    CHOICE_NEWS_OR_ARTICLE = [(1, 'News'), (2, 'Article')]
    news_or_article = models.IntegerField(choices=CHOICE_NEWS_OR_ARTICLE) # choises- список или кортеж,первым хранит значение, хранимое в БД, второй отображается виджетом формы
    header = models.CharField(max_length=255) # Первичный ключ доступен только для чтения
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='PostCategory')

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def preview(self):
        return self.text[:124] + "..."

    def like(self):
        self.rating += 1
        self.save() # Родительский метод, вызывается для корректного сохранения объекта в БД

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()





