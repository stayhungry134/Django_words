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
def shanbay_article_list():
    from reading.shanbay import Article
    article = Article()
    article.get_article_list()


@shared_task
def shanbay_article_content():
    from reading.shanbay import Article
    article = Article()
    article.get_article_content()


@shared_task
def magazine_sync_task():
    from reading.magazine import MagazineSync
    magazine_sync = MagazineSync()
    magazine_sync.sync()


@shared_task
def generate_magazine_cover():
    """
    生成杂志封面
    """
    from reading.magazine import MagazineSync
    magazine_sync = MagazineSync()
    magazine_sync.generate_cover()
