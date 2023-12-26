"""
name: models
create_time: 2023/12/26 10:02
author: Ethan

Description: 
"""
from django.db import models

from base.model import BaseModel
from mdeditor.fields import MDTextField


class Article(BaseModel):
    title = models.CharField(max_length=128, verbose_name='文章标题')
    content = MDTextField(verbose_name='文章内容')
    last_review = models.DateField(verbose_name='上次复习日期')

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title