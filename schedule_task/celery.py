"""
name: celery
create_time: 2023/12/26 9:56
author: Ethan

Description: 配置一些定时任务
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_words.settings')

# 创建celery应用
app = Celery('django_words')

# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有已注册的app中加载任务模块
app.autodiscover_tasks()