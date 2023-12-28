"""
name: views
create_time: 2023/12/25 10:40
author: Ethan

Description: 
"""
import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from word.models import NewWord, ReviewRecord
from word.serializers import NewWordSerializer, ReviewRecordSerializer


class NewWordView(APIView):
    """用于处理新词的视图"""
    pass


class WordView(APIView):
    def get(self, request):
        import requests

        from word.utils import remind_word
        word = request.GET.get('word', '')
        if word == '':
            raise "word 参数不能为空"
        word_data = NewWord.objects.filter(word=word).first()
        if word_data:
            remind_word(word_data)
            return Response(word_data.meaning)
        url = 'https://dict.youdao.com/jsonapi_s'
        params = {
            'doctype': 'json',
            'jsonversion': 4,
        }
        data = {
            'q': word,
            'le': 'en',
            't': 2,
            'client': 'web',
            'sign': '4f3b645c416fd42cfec797713b4f5aa4',
            'keyfrom': 'webdict',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Host': 'dict.youdao.com',
            'Referer': 'https://dict.youdao.com/result'
        }
        word_data = requests.post(url=url, params=params, headers=headers, data=data).json()
        meaning = word_data['ec']['word']['trs']
        # 柯林斯解释
        collins = word_data['collins']['collins_entries']
        new_word = NewWord(
            word=word,
            meaning=meaning,
            collins=collins,
            tag=NewWord.TAG_ARTICLE,
            uk_audio=f'https://dict.youdao.com/dictvoice?audio={word}&type=1',
            us_audio=f'https://dict.youdao.com/dictvoice?audio={word}&type=2',
        )
        new_word.save()
        remind_word(new_word)
        return Response(meaning)

