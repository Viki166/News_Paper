from django.urls import path
from .views import *

urlpatterns = [
    path('', Postlist.as_view()), # Список всех новостей
    # path('<int:pk>', PostDetail.as_view()),
    path('search', SearchList.as_view(), name='search'), # Список новостей и их сортировка
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Детальная новость
    path('add/', PostCreateView.as_view(), name='post_create'), # Создание новости
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # Удаление новости
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'), # Редактирование новости
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscribe/<int:pk>', Subscribe.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>', UnSubscribe.as_view(), name='unsubscribe'),
]