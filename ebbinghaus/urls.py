from django.urls import path
from ebbinghaus import views

app_name = 'ebbinghaus'


urlpatterns = [
    path('word/', views.LearnWordsView.as_view(), name='learn_words'),
    path('put_words/', views.PutWordsView.as_view(), name='put_words'),
    path('articles/', views.Articles.as_view(), name='articles'),
    path('article/<int:id>/', views.Article.as_view(), name='article'),
    path('put_article/', views.Article.as_view(), name='put_article'),
]
