"""
name: serializers
create_time: 2023/12/27 10:19
author: Ethan

Description: 
"""
from rest_framework import serializers

from base.serializers import BaseModelSerializer
from reading.models import Article


class CategoryField(serializers.RelatedField):
    """
    自定义分类字段
    """
    def to_representation(self, value):
        return {
            'id': value.id,
            'key': value.key,
            'description': value.name
        }


class TextFieldToJSONField(serializers.JSONField):
    """
    将TextField的值转换为JSON格式
    """

    def to_representation(self, value):
        import re
        # 将TextField的值转换为JSON格式
        paragraphs = re.split(r'\n+', value)
        paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph]
        article_words = [paragraph.split(' ') for paragraph in paragraphs if paragraph]
        return serializers.JSONField().to_representation(article_words)


class ArticleSerializer(BaseModelSerializer):
    category = CategoryField(read_only=True)
    last_review = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    content = TextFieldToJSONField()

    class Meta:
        model = Article
        fields = (
            'id', 'title_en', 'title_cn', 'summary', 'content', 'image', 'category', 'create_time', 'last_review',
            'length')
        content_type = 'application/json'


class ArticleListSerializer(BaseModelSerializer):
    category = CategoryField(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id', 'title_en', 'title_cn', 'image', 'create_time', 'length')
        content_type = 'application/json'
