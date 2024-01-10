"""
name: views
create_time: 2023/12/27 10:19
author: Ethan

Description: 
"""
import datetime

from django.core.paginator import Paginator
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
            article = Article.objects.filter(Q(last_review__lte=today) | Q(last_review__isnull=True)).first()
        else:
            article = Article.objects.filter(id=article_id).first()
        if not article:
            return None
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def post(self, request):
        """
        用于处理文章的试图
        :param request:
        :return:
        """
        handle = request.data.get('handle', None)
        article_id = request.data.get('article_id', None)
        if not handle:
            return Response({'msg': 'handle 参数不能为空'})
        if not article_id:
            return Response({'msg': 'id 参数不能为空'})
        article = Article.objects.filter(id=article_id).first()
        if not article:
            return Response({'msg': '文章不存在'})
        if handle == 'review':
            article.review()

        return Response({'msg': 'success'})


class ArticlesView(APIView):
    """
    用于处理文章列表相关的请求
    """
    def get(self, request):
        articles = Article.objects.all().order_by('-last_review')
        page_size = request.GET.get('page_size', 10)
        page = request.GET.get('page', 1)
        res_pager = Paginator(articles, page_size).get_page(page)
        serializer = ArticleSerializer(res_pager, many=True, context={'res_type': 'list'})

        return Response({
            'page': page,
            'has_previous': res_pager.has_previous(),
            'has_next': res_pager.has_next(),
            'total': articles.count(),
            'items': serializer.data,
            'page_num': res_pager.paginator.num_pages,
            'page_size': page_size,
        })
