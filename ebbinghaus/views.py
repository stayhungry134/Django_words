import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
import markdown

from ebbinghaus.models import LearnWords, TodayArticle


# Create your views here.
def index(request):
    """主页"""
    # 重定向到今日单词
    return redirect('ebbinghaus:words')


def get_words(request):
    """获取今日单词"""
    today = datetime.date.today()
    if request.method == 'POST':
        for word_form in request.POST:
            word = LearnWords.objects.filter(word=word_form).first()
            if word:
                review_index = eval(request.POST[word_form][0])
                review_list = word.get_review_times
                # print(review_list)
                review_list[review_index-1] = True
                # print(review_list)
                word.review_times = review_list
                word.last_review = today
                word.save()
    words = LearnWords.objects.filter(next_date__lte=today)[:30]
    return render(request, 'ebbinghaus/ebbinghaus.html', locals())


def get_article(request, article_id):
    """获取文章"""
    article = TodayArticle.objects.filter(id=article_id).first()
    # 更新文章复习时间
    article.last_review = datetime.date.today()
    article.save()

    date = article.init_date
    article.content = markdown.Markdown().convert(article.content)
    # 使用 span 标签包裹单词
    article.content = article.content.replace(' ', '</span> <span class="word">')
    article.content = article.content.replace(',</span>', '</span>, ')
    article.content = article.content.replace('.</span>', '</span>. ')
    article.content = article.content.replace('<p>', '<p class="my-3"><span class="word">')
    article.content = article.content.replace('</p>', '</span></p>')
    # 查询date的单词
    words = LearnWords.objects.filter(init_date=date)
    # 将文章中的今日单词标记出来
    for word in words:
        article.content = article.content.replace(f'<span class="word">{word.word}', f'<span class="word today-word">{word.word}')
    return render(request, 'ebbinghaus/article.html', locals())


def get_translate(request, word):
    """获取单词翻译"""
    import yaml
    from .utils import get_word_translation
    translation = get_word_translation(word)
    return JsonResponse(translation)
