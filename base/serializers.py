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
    def __init__(self, model=None, fields=None, **kwargs):
        self.Meta.model = model
        if fields:
            self.Meta.fields = fields
        elif hasattr(model, 'serializable_fields'):
            self.Meta.fields = model.serializable_fields
        else:
            self.Meta.fields = '__all__'
        super().__init__()

    class Meta:
        content_type = 'application/json'

    def save(self, **kwargs):
        pass

    def update(self, instance, validated_data):
        pass
