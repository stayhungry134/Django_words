from django.contrib import admin
from .models import LearnWords, LearnArticle


# Register your models here.
class TodayArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('标题', {'fields': ['title']}),
        ('内容', {'fields': ['content']}),
        ('日期', {'fields': ['last_review']}),
    ]


admin.site.register(LearnWords)
admin.site.register(LearnArticle, TodayArticleAdmin)
