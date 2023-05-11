from django.contrib import admin
from .models import LearnWords, TodayArticle

# Register your models here.
admin.site.register(LearnWords)
admin.site.register(TodayArticle)