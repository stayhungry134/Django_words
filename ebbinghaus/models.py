from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField


# Create your models here.
class LearnWords(models.Model):
    word = models.CharField(max_length=128, verbose_name='单词', db_index=True, unique=True)
    definition = models.JSONField(max_length=512, verbose_name='词义')
    init_date = models.DateField(verbose_name='单词初始化时间', db_index=True)
    last_review = models.DateField(blank=True, null=True, verbose_name='上次复习时间')
    next_date = models.DateField(verbose_name='下次学习单词时间', db_index=True)
    uk_audio = models.CharField(max_length=256, verbose_name='英式发音')
    us_audio = models.CharField(max_length=256, verbose_name='美式发音')
    familiarity = models.IntegerField(verbose_name='熟悉程度', default=0)
    # 复习时间列表 [1, 2, 4, 7, 15, 30, 60, 90, 180]
    review_times = models.JSONField(verbose_name='复习时间列表', default=[False] * 9)
    # review_times = ArrayField(models.BooleanField(default=False, verbose_name='复习日期'), size=9)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'learn_word'

    # 重写 save 函数
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        import datetime
        today = datetime.date.today()
        if not self.init_date:
            self.init_date = today
        self.next_date = today
        reviews = self.review_times

        # 保证前面的天数复习完，才能出现后面的天数
        for i, date in enumerate(reviews):
            if i == 0:
                continue
            reviews[i] = date and reviews[i - 1]

        # 计算下一次复习的时间
        review_list = [1, 2, 4, 7, 15, 30, 60, 90, 180]
        for i, date in enumerate(reviews[::-1]):
            if date:
                self.next_date = today + datetime.timedelta(days=review_list[-i-1])
                break

        # 如果没有上次复习时间，就设置为初始化时间
        if not self.last_review:
            self.last_review = self.init_date.isoformat()

        return super().save(force_insert=force_insert,
                            force_update=force_update,
                            using=using,
                            update_fields=update_fields)


class TodayArticle(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    content = MDTextField(verbose_name='内容')
    init_date = models.DateField(auto_now_add=True, verbose_name='生成日期')
    last_review = models.DateField(verbose_name='上次复习日期')

    def __str__(self):
        return f"{self.title}---{self.init_date.isoformat()}"

    class Meta:
        verbose_name = 'today_article'
