from django.forms import ModelForm
from django import forms
from .models import Post


class PostForm(ModelForm):
    # дополнительные настройки, включает все,что не является полем(сортировка, название таблицы БД..)
    class Meta:
        model = Post
        fields = ['author', 'news_or_article', 'text', 'categories', 'header']