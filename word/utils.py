"""
name: utils
create_time: 2023/12/25 10:09
author: Ethan

Description: 
"""
from word.models import NewWord, ReviewRecord
import datetime


def remind_word(word: NewWord):
    """
    重新记忆单词，将单词熟练度置为 1
    :param word: word 是一个NewWord 对象
    :return:
    """
    # 保存到记忆记录当中
    record = ReviewRecord.objects.filter(word=word).first() or ReviewRecord(word=word)
    record.familiarity = 1
    record.save()


def review_word(word: NewWord):
    """
    复习单词，将单词熟练度 + 1
    :param word: word 是一个NewWord 对象
    :return:
    """
    # 保存到记忆记录当中
    record = ReviewRecord.objects.filter(word=word).first() or ReviewRecord(word=word)
    record.familiarity += 1
    record.save()