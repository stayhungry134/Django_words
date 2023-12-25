"""
name: urls
create_time: 2023/12/25 13:51
author: Ethan

Description: 
"""
from django.urls import path
from word import views

app_name = 'word'


urlpatterns = [
    path('word/', views.WordView.as_view(), name='word'),
]
