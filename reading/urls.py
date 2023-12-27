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
    path('article/', views.ArticleView.as_view(), name='文章'),
]