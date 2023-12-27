"""
name: views
create_time: 2023/12/27 10:19
author: Ethan

Description: 
"""
import datetime

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from reading.models import Article
from reading.serializers import ArticleSerializer


class ArticleView(APIView):
    """
    用于处理文章相关的请求
    """
    def get(self, request):
        article_id = request.query_params.get('id', None)
        if not article_id:
            today = datetime.date.today()
            article = Article.objects.filter(   Q(last_review__lte=today) | Q(last_review__isnull=True)).first()
        else:
            article = Article.objects.filter(id=article_id).first()
        if not article:
            return None
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
