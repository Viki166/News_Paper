from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Post(models.Model):
    CHOICE_NEWS_OR_ARTICLE = [(1, 'News'), (2, 'Article')]
    news_or_article = models.IntegerField(choices=CHOICE_NEWS_OR_ARTICLE)
    header = models.CharField(max_length=255)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + "..."


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
