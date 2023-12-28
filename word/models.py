"""
name: model
create_time: 2023/12/22 16:27
author: Ethan

Description: 
"""
import datetime

from django.db import models

from base.model import BaseModel
from mdeditor.fields import MDTextField


class NewWord(BaseModel):
    TAG_SHANBAY = 'shanbay'
    TAG_ARTICLE = 'article'
    TAG_BOOK = 'book'
    TAG_OTHER = 'other'
    TAG_CHOICES = (
        (TAG_SHANBAY, '扇贝'),
        (TAG_ARTICLE, '文章'),
        (TAG_BOOK, '书籍'),
        (TAG_OTHER, '其他'),
    )
    word = models.CharField(max_length=50, unique=True, verbose_name='单词', db_index=True)
    meaning = models.JSONField(verbose_name='释义')
    collins = models.JSONField(null=True, blank=True, verbose_name='柯林斯词典')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default=TAG_OTHER, verbose_name='标签')
    uk_audio = models.CharField(max_length=200, null=True, blank=True, verbose_name='英式发音')
    us_audio = models.CharField(max_length=200, null=True, blank=True, verbose_name='美式发音')
    notes = MDTextField(verbose_name='笔记')

    class Meta:
        verbose_name = '新单词'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.word


def review_times_default():
    """
    默认的复习时间列表
    :return:
    """
    return []


class ReviewRecord(models.Model):
    word = models.OneToOneField(NewWord, on_delete=models.CASCADE, verbose_name='单词')
    last_review = models.DateField(null=True, blank=True, verbose_name='上次复习时间')
    next_review = models.DateField(null=True, blank=True, verbose_name='下次复习时间')
    familiarity = models.IntegerField(default=0, verbose_name='熟悉程度')
    review_times = models.IntegerField(default=0, verbose_name='复习次数')
    review_times_list = models.JSONField(default=review_times_default, verbose_name='复习时间列表')

    class Meta:
        verbose_name = '复习记录'
        verbose_name_plural = verbose_name
        ordering = ('-next_review',)

    def __str__(self):
        return self.word

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # 记忆次数加 1
        self.review_times += 1
        # 相隔的天数，
        today = datetime.date.today()
        self.last_review = today
        interval = int(1.8 ** self.familiarity)
        self.next_review = today + datetime.timedelta(days=interval)
        times_list: list = self.review_times_list or review_times_default()
        times_list.append(today.isoformat())
        self.review_times_list = times_list

        return super().save(force_insert=force_insert,
                            force_update=force_update,
                            using=using,
                            update_fields=update_fields)

