"""
name: utils
create_time: 2023/12/25 10:09
author: Ethan

Description: 
"""
from word.models import NewWord, ForgettingCurve
import datetime


def remind_word(word: NewWord):
    """
    记忆单词，更新记忆单词
    :param word: word 是一个NewWord 对象
    :return:
    """
    # 保存到记忆记录当中
    today = datetime.date.today()

    curve = ForgettingCurve.objects.filter(word=word).first() or ForgettingCurve(word=word)
    curve.last_review = today
    curve.save()