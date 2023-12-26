"""
name: tasks
create_time: 2023/12/26 13:17
author: Ethan

Description: 
"""
# your_app/tasks.py
import logging

from celery import shared_task
from datetime import datetime, timedelta


@shared_task
def shanbay_article():
    from shanbay import Article
    article = Article()
    article.get_article_list()
