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
    image = models.ImageField(upload_to='article', blank=True, null=True, verbose_name='文章图片')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='文章分类')
    source = models.CharField(max_length=128, default='shanbay', verbose_name='文章来源')
    third_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='第三方文章key')
    last_review = models.DateField(blank=True, null=True, verbose_name='上次复习日期')
    length = models.IntegerField(blank=True, null=True, verbose_name='文章长度')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title_en


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