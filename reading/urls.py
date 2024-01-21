"""
name: urls
create_time: 2023/12/26 13:16
author: Ethan

Description: 
"""
from django.urls import path
from reading import views

app_name = 'reading'


urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='分类'),
    path('article/', views.ArticleView.as_view(), name='文章'),
    path('articles/', views.ArticlesView.as_view(), name='文章列表'),
    path('magazine/', views.MagazineView.as_view(), name='杂志'),
    path('books/', views.BooksView.as_view(), name='书籍列表'),
    path('book/', views.BookView.as_view(), name='书籍'),
    path('book/chapter/', views.ChapterView.as_view(), name='章节'),
]