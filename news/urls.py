from django.urls import path
from .views import *

urlpatterns = [
    path('', Postlist.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', SearchList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
]