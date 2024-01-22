"""
name: serializers
create_time: 2023/12/27 10:19
author: Ethan

Description: 
"""
from rest_framework import serializers

from base.serializers import BaseModelSerializer
from reading.models import Article, Magazine, Book, Chapter, Content


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
        fields = ('id', 'title_en', 'title_cn', 'image', 'create_time', 'length')
        content_type = 'application/json'


class MagazineSerializer(BaseModelSerializer):
    category = CategoryField(read_only=True)

    class Meta:
        model = Magazine
        fields = ('id', 'name', 'local_path', 'category', 'cover', 'create_time', 'update_time')


class ContentSerializer(BaseModelSerializer):
    class Meta:
        model = Content
        fields = ('id', 'chapter', 'content')


class ChapterSerializer(BaseModelSerializer):

    class Meta:
        model = Chapter
        fields = ('id', 'book', 'title_cn', 'title_en', 'create_time', 'update_time', 'index', 'is_finished', 'length')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('res_type') == 'detail':
            data['content'] = ContentSerializer(instance.content).data
        return data


class BookListSerializer(BaseModelSerializer):
    category = CategoryField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title_cn', 'category', 'cover', 'create_time', 'update_time', 'short_description')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        total_chapters = instance.chapter_set.count()
        # 已完成的章节数
        """
        在 Django 中，如果你有一个模型 Book，并且有一个多对一（ManyToOne）的关系到另一个模型 Chapter，Django 会为 Book 模型自动创建一个反向关系。这个反向关系默认使用模型名小写 + _set 的方式命名。
        """
        completed_chapters = instance.chapter_set.filter(is_finished=True).count()

        # 计算完成百分比
        if total_chapters > 0:
            completion_percentage = (completed_chapters / total_chapters) * 100
        else:
            completion_percentage = 0

        data['completion_percentage'] = completion_percentage
        return data


class BookSerializer(BaseModelSerializer):
    category = CategoryField(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title_cn', 'title_en', 'category', 'cover', 'create_time', 'update_time', 'description',
                  'author', 'short_description', 'chapters')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['chapters'] = ChapterSerializer(instance.chapter_set.all(), many=True).data
        return data
