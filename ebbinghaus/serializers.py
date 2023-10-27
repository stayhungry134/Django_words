"""
name: serializers
create_time: 2023/5/17
author: Ethan

Description: 
"""
from rest_framework import serializers

from ebbinghaus.models import LearnWords, LearnArticle


class LearnWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnWords
        fields = ('id', 'word', 'definition', 'uk_audio', 'us_audio', 'familiarity', 'review_times')
        content_type = 'application/json'

    def save(self, **kwargs):
        word = self.validated_data['word']
        if LearnWords.objects.filter(word=word).first():
            LearnWords.objects.filter(word=word).update(**self.validated_data)
        else:
            LearnWords.objects.create(**self.validated_data)

    def update(self, **kwargs):
        word = self.validated_data['word']
        review_times = self.validated_data['review_times']
        LearnWords.objects.filter(word=word).update(review_times=review_times)


class TextFieldToJSONField(serializers.JSONField):
    def to_representation(self, value):
        import re
        # 将TextField的值转换为JSON格式
        paragraphs = re.split(r'\n+', value)
        article_words = [paragraph.split(' ') for paragraph in paragraphs]
        return serializers.JSONField().to_representation(article_words)


class TodayArticleSerializer(serializers.ModelSerializer):
    content = TextFieldToJSONField()
    class Meta:
        model = LearnArticle
        fields = ('id', 'title', 'content', 'init_date', 'last_review')
        content_type = 'application/json'