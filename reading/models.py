"""
name: models
create_time: 2023/12/26 10:02
author: Ethan

Description: 
"""
from django.db import models

from base.model import BaseModel
from mdeditor.fields import MDTextField


class Category(BaseModel):
    """文章分类"""
    CLASSIFY = (
        ('article', '阅读'),
        ('magazine', '杂志'),
        ('book', '书籍'),
    )
    classify = models.CharField(max_length=128, choices=CLASSIFY, verbose_name='分类', default='article')
    key = models.CharField(max_length=128, verbose_name='分类key', unique=True, db_index=True)
    name = models.CharField(max_length=128, verbose_name='分类名称')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    """文章"""
    title_cn = models.CharField(max_length=256, blank=True, null=True,  verbose_name='文章中文标题')
    title_en = models.CharField(max_length=256, verbose_name='文章英文标题')
    summary = models.CharField(max_length=1024, blank=True, null=True, verbose_name='文章摘要')
    content = MDTextField(verbose_name='文章内容')
    image = models.ImageField(upload_to='article_img', blank=True, null=True, verbose_name='文章图片')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='文章分类')
    source = models.CharField(max_length=128, default='shanbay', verbose_name='文章来源')
    third_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='第三方文章key')
    last_review = models.DateTimeField(blank=True, null=True, verbose_name='上次复习时间')
    length = models.IntegerField(blank=True, null=True, verbose_name='文章长度')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return self.title_en

    def review(self):
        """
        复习文章
        :return:
        """
        import datetime
        self.last_review = datetime.datetime.now()
        self.save()


class Magazine(BaseModel):
    """杂志"""
    name = models.CharField(max_length=128, verbose_name='杂志名称')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='杂志分类')
    cover = models.ImageField(upload_to='magazine_cover', blank=True, null=True, verbose_name='杂志封面')
    local_path = models.FileField(upload_to='magazine', blank=True, null=True, verbose_name='杂志文件')
    remote_path = models.CharField(max_length=256, verbose_name='杂志路径', db_index=True)

    class Meta:
        verbose_name = '杂志'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Book(BaseModel):
    title_cn = models.CharField(max_length=255, verbose_name='中文标题')
    title_en = models.CharField(max_length=255, verbose_name='英文标题')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='书籍分类', null=True)
    cover = models.ImageField(upload_to='reading/book/book_cover', verbose_name='封面')
    third_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='第三方id')
    description = models.TextField(blank=True, null=True, verbose_name='简介')
    short_description = models.CharField(max_length=255, blank=True, null=True, verbose_name='简短简介')
    author = models.CharField(max_length=128, blank=True, null=True, verbose_name='作者')

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return self.title_en


class Chapter(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍', db_index=True)
    index = models.IntegerField(verbose_name='章节序号')
    title_cn = models.CharField(max_length=255, verbose_name='中文标题')
    title_en = models.CharField(max_length=255, verbose_name='英文标题')
    third_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='第三方id')
    length = models.IntegerField(blank=True, null=True, verbose_name='文章长度')
    is_finished = models.BooleanField(default=False, verbose_name='是否完成阅读')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ('book', 'index',)

    def __str__(self):
        return self.title_en


class Content(BaseModel):
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE, verbose_name='章节', db_index=True)
    content = models.JSONField(verbose_name='内容', default=[])

    class Meta:
        verbose_name = '内容'
        verbose_name_plural = verbose_name