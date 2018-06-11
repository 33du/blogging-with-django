from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tag_name>/', views.index, name='index'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('comment/delete/', views.delete_comment, name='delete comment'),
]
