from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import render
from .models import Author, Post, Category, Comment
from .filters import PostFilter
from .forms import PostForm


class Postlist(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.order_by('-id')
# Manager(object)- самый важный атрибут модели. Это интерфейс, через который django выполняет запросы к БД и получает объекты


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 0
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Родительский метод, вызывается для корректного сохранения объекта в БД
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):# дополнительные аргументы для методов
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm

    def get_object(self,**kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/search/'