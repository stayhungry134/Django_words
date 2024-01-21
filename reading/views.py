"""
name: views
create_time: 2023/12/27 10:19
author: Ethan

Description: 
"""
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from reading.models import Article, Magazine, Category, Book, Chapter
from reading.serializers import ArticleSerializer, MagazineSerializer, BookListSerializer, BookSerializer, \
    ChapterSerializer


class CategoryView(APIView):
    """
    用于处理文章分类相关的请求
    """

    def get(self, request):
        category_classify = request.query_params.get('classify', None)
        if not category_classify:
            return Response({'msg': '分类不能为空'})
        category = Category.objects.filter(classify=category_classify).all().values('id', 'key', 'name')
        if not category:
            return Response({'msg': '分类不存在'})
        return Response({
            'items': category
        })


class ArticleView(APIView):
    """
    用于处理文章相关的请求
    """

    def get(self, request):
        article_id = request.query_params.get('id', None)
        if not article_id:
            article = (Article.objects.filter().order_by('last_review').first())
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
        articles = Article.objects.all().order_by('last_review')
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


class MagazineView(APIView):
    """
    用于处理杂志相关的请求
    """

    def get(self, request):
        magazine_id = request.query_params.get('id', None)
        if not magazine_id:
            page_size = request.GET.get('page_size', 12)
            page = request.GET.get('page', 1)
            category_id = request.GET.get('category_id', None)
            if not category_id:
                category = Category.objects.filter(classify='magazine').first()
            else:
                category = Category.objects.filter(id=category_id).first()
            magazines = Magazine.objects.filter(category=category).all().order_by('-id')
            res_pager = Paginator(magazines, page_size).get_page(page)
            serializer = MagazineSerializer(res_pager, many=True)
            return Response({
                'page': page,
                'has_previous': res_pager.has_previous(),
                'has_next': res_pager.has_next(),
                'total': magazines.count(),
                'items': serializer.data,
                'page_num': res_pager.paginator.num_pages,
                'page_size': page_size,
            })
        else:
            magazine = Magazine.objects.filter(id=magazine_id).first()
        if not magazine:
            return None
        serializer = MagazineSerializer(magazine)
        return Response({
            'magazine': serializer.data
        })

    def post(self, request):
        """
        用于处理杂志的试图
        :param request:
        :return:
        """
        from django_words.settings import MEDIA_ROOT
        files = request.FILES.getlist('file', None)
        if not files:
            return Response({'msg': '文件不能为空'})
        file_name = request.POST.get('name', None)
        with open(f"{MEDIA_ROOT}/reading/magazine/{file_name}", 'wb') as f:
            for file in files:
                for chunk in file.chunks():
                    f.write(chunk)
        return Response({'msg': 'success'})


class BooksView(APIView):
    def get(self, request):
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 12)
        category_id = request.GET.get('category_id', None)
        if not category_id:
            category = Category.objects.filter(classify='book').first()
        else:
            category = Category.objects.filter(id=category_id).first()
        books = Book.objects.filter(category=category)
        res_pager = Paginator(books, page_size).get_page(page)
        serializer = BookListSerializer(res_pager, many=True)
        return Response({
            'page': page,
            'has_previous': res_pager.has_previous(),
            'has_next': res_pager.has_next(),
            'total': books.count(),
            'items': serializer.data,
            'page_num': res_pager.paginator.num_pages,
            'page_size': page_size,
        })


class BookView(APIView):
    def get(self, request):
        book_id = request.query_params.get('id', None)
        if not book_id:
            return Response({'msg': 'id 不能为空'})
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response({'msg': '书籍不存在'})
        serializer = BookSerializer(book)
        return Response(serializer.data)


class ChapterView(APIView):
    def get(self, request):
        chapter_id = request.query_params.get('id', None)
        if not chapter_id:
            return Response({'msg': 'id 不能为空'})
        chapter = Chapter.objects.filter(id=chapter_id).first()
        if not chapter:
            return Response({'msg': '章节不存在'})
        serializer = ChapterSerializer(chapter, context={'res_type': 'detail'})
        return Response(serializer.data)