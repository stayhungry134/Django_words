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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='文章分类')
    source = models.CharField(max_length=128, default='shanbay', verbose_name='文章来源')
    third_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='第三方文章key')
    last_review = models.DateTimeField(blank=True, null=True, verbose_name='上次复习时间')
    length = models.IntegerField(blank=True, null=True, verbose_name='文章长度')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

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

    def __str__(self):
        return self.name


# class Book(BaseModel):
#     title = models.CharField(max_length=255)
#     publication_date = models.DateField()
#     auther = models.CharField(max_length=128)
#
#
# class Chapter(BaseModel):
#     title = models.CharField(max_length=255)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#
#
# class Content(BaseModel):
#     content_text = models.TextField()
#     chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)