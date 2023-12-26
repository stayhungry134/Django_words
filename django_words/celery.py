"""
name: celery
create_time: 2023/12/26 9:56
author: Ethan

Description: 配置一些定时任务
1. 确保有安装Celery、Redis等常用的Python扩展库
2. windows下执行运行Worker，任务不执行，必需使用-P eventlet启动，同时连接Redis必需使用IP地址，不能使用localhost
3. 启动Worker时必需和消息队列保持连通，修改任务函数后，必需重启Worker
4. 启动Worker时可以指定消息队列，但是必需在配置文件中配置，或调用任务时指定队列名
5. 如果都是使用默认队列celery，启动Worker时可能会收到大量历史任务并进行处理
6. 定时任务celery beat如果没有及时关闭，会一直按要求发送异步任务，产生大量历史遗留任务
"""
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