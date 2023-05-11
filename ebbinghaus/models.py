from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField


# 验证器，验证一个只包含布尔值的列表
def validate_bool_list(value_list):
    if isinstance(value_list, list):
        if len(value_list) == 9:
            raise ValidationError(_(f"{value_list}必须是9个元素"), params={'value_list': value_list})
        for i in value_list:
            if not isinstance(i, bool):
                raise ValidationError(_(f"列表中{i}元素不是布尔类型"), params={'i': i})
    else:
        raise ValidationError(_(f"{value_list}必须为一个列表"), params={'value_list': value_list})


# Create your models here.
class LearnWords(models.Model):
    word = models.CharField(max_length=128, verbose_name='单词')
    meaning = models.CharField(max_length=512, verbose_name='词义')
    init_date = models.DateField(auto_now_add=True, verbose_name='初次学习单词时间')
    last_review = models.DateField(blank=True, null=True, verbose_name='上次复习时间')
    next_date = models.DateField(verbose_name='下次学习单词时间')
    # 复习时间列表 [1, 2, 4, 7, 15, 30, 60, 90, 180]
    review_times = models.CharField(validators=[validate_bool_list], max_length=256, verbose_name='复习时间列表')
    # review_times = ArrayField(models.BooleanField(default=False, verbose_name='复习日期'), size=9)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'learn_word'

    # 重写 save 函数
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        import datetime
        today = datetime.date.today()
        reviews = eval(self.review_times)

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

    # 获取复习时间列表
    @property
    def get_review_times(self):
        return eval(self.review_times)


class TodayArticle(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    content = MDTextField(verbose_name='内容')
    init_date = models.DateField(auto_now_add=True, verbose_name='生成日期')
    last_review = models.DateField(verbose_name='上次复习日期')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'today_article'
