from django.urls import path
from ebbinghaus import views

app_name = 'ebbinghaus'


urlpatterns = [
    path('', views.index, name='index'),
]
