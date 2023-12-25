"""
name: serializers
create_time: 2023/5/17
author: Ethan

Description: 
"""
from rest_framework import serializers

from base.serializers import BaseModelSerializer
from word.models import NewWord, ForgettingCurve


class NewWordSerializer(BaseModelSerializer):
    class Meta:
        model = NewWord
        fields = ('id', 'word', 'meaning', 'collins', 'uk_audio', 'us_audio')
        content_type = 'application/json'


class ForgettingCurveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgettingCurve
        fields = ('word', 'last_review', 'next_review', 'familiarity', 'review_times')
        content_type = 'application/json'
