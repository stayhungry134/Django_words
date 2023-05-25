from django.urls import path
from ebbinghaus import views

app_name = 'ebbinghaus'


urlpatterns = [
    path('words/', views.LearnWordsView.as_view(), name='learn_words'),
    path('put_words/', views.PutWordsView.as_view(), name='put_words'),
]
