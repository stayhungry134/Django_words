from django.urls import path
from ebbinghaus import views

app_name = 'ebbinghaus'


urlpatterns = [
    path('', views.index, name='index'),
    path('words/', views.get_words, name='words'),
    # 文章路由，携带参数id
    path('article/<int:article_id>/', views.get_article, name='article'),
    # 请求单词翻译
    path('translate/<slug:word>/', views.get_translate, name='translate'),
]
