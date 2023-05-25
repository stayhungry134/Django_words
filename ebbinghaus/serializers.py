"""
name: serializers
create_time: 2023/5/17
author: Ethan

Description: 
"""
from rest_framework import serializers

from ebbinghaus.models import LearnWords


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