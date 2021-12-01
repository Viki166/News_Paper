from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.decorators import login_required
# Class-based views — представления, организованные в виде классов.
# Generic class-based views — часто используемые представления, которые Django предлагает в виде решения «из коробки». Они реализуют в первую очередь функционал CRUD (Create Read Update Delete).


# Список всех новостей
class Postlist(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.order_by('-id')


# Подробное представление новости
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


# Сортировка новостей по дате и имени автора
class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 0
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


# Дженерик для получения детальной новости
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


# Дженерик для создания новости
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = 'news.add_author'


# Дженерик для редактирования новости
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = 'news.change_author'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# Дженерик для удаления новости
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/search/'
    permission_required = 'news.delete_author'


# Идентификация пользователя
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/news')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            common_group = Group.objects.get(name='common')
            common_group.user_set.add(user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/news')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


# декоратор проверки аутентификации
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/search')


# Выйти из аккаунта
def user_logout(request):
    logout(request)
    return redirect('/news')



