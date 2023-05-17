from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('words/', views.LearnWordsView.as_view(), name='learn_words'),
]