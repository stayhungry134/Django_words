from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator


# Create your views here.
class LearnWordsView(APIView):
    """学习单词的试图"""
    def get(self, request):
        import re
        import datetime
        from ebbinghaus.models import LearnWords
        from .serializers import LearnWordsSerializer

        today = datetime.date.today()
        queryset = LearnWords.objects.filter(next_date__lte=today)
        # 分页
        page_size = request.GET.get('page_size', 30)
        page = request.GET.get('page', 1)
        words_data = Paginator(queryset, page_size).get_page(page)

        serializer = LearnWordsSerializer(words_data, many=True)
        # 重写序列化器的definition字段
        for data in serializer.data:
            # 将词义中符合正则表达式的部分加上标签
            data['definition'] = [re.sub(r'(\w+\.)', r'<span style="color: #ea7a71">\1</span>', definition)
                                  for definition in data['definition']]
        total_count = queryset.count()
        response = {
            'total_count': total_count,
            'word': {word_item['word']: word_item for word_item in serializer.data},
        }
        return Response(response)

    def post(self, request):
        """提交每日单词复习情况的视图"""
        from .models import LearnWords
        for word_data in request.data.values():
            word = word_data.get('word')
            review_times = word_data.get('review_times')
            word = LearnWords.objects.filter(word=word).first()
            word.review_times = review_times
            word.save()
        return Response("你更新了我")


class PutWordsView(APIView):
    """提交每日单词的视图"""
    def get(self, request):
        return Response("我被调用了")

    def post(self, request):
        from .serializers import LearnWordsSerializer
        for word_data in request.data.values():
            serializer = LearnWordsSerializer(data=word_data)
            if serializer.is_valid():
                serializer.save()
            else:
                import logging
                logger = logging.getLogger('ebbinghaus')
                logger.info(f"{word_data}")
                logger.info(serializer.errors)  
        return Response("你提交了一个post请求")


class Articles(APIView):
    """用于处理文章列表的视图"""
    pass


class Article(APIView):
    """用于处理文章的视图"""
    def get(self, request, id):
        from django.shortcuts import get_object_or_404
        from .serializers import TodayArticleSerializer
        from .models import LearnArticle
        article = get_object_or_404(LearnArticle, pk=id)
        if not article:
            return Http404
        serializer = TodayArticleSerializer(article)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        if not request.data or not request.data.get('word'):
            return Response("你提交了一个空的post请求")
        words = request.data.get('word')

        return Response("我被调用了")
