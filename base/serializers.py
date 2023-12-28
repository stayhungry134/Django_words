"""
name: serializers
create_time: 2023/12/25 10:52
author: Ethan

Description: 序列化的基类
"""
from abc import ABC, abstractmethod

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    序列化的基类
    """
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')