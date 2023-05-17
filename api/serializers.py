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
        fields = ('id', 'word', 'meaning', 'init_date', 'get_review_times')
        content_type = 'application/json'
