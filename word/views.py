"""
name: views
create_time: 2023/12/25 10:40
author: Ethan

Description: 
"""
import datetime
import re

from django.core.paginator import Paginator
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
        # 去除单词两边的符号
        word = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', word)
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
        collins = None
        try:
            collins = word_data['collins']['collins_entries'][0]['entries']['entry']
        except:
            pass
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


class RemindView(APIView):
    """
    记忆单词
    """

    def get(self, request):
        """
        获取单词列表
        :param request:
        :return:
        """
        # 获取今天需要复习的单词
        today = datetime.date.today()
        page_size = request.GET.get('page_size', 20)
        page = request.GET.get('page', 1)
        today_words = ReviewRecord.objects.filter(next_review__lte=today)
        res_pager = Paginator(today_words, page_size).get_page(page)
        serializer = ReviewRecordSerializer(res_pager, many=True)
        return Response({
            'page': page,
            'has_previous': res_pager.has_previous(),
            'has_next': res_pager.has_next(),
            'total': today_words.count(),
            'items': serializer.data,
            'page_num': res_pager.paginator.num_pages,
            'page_size': page_size,
        })

    def post(self, request):
        """
        记忆单词
        :param request:
        :return:
        """
        from word.utils import review_word

        word_list = request.data.get('word_list')
        if not word_list:
            return Response('word_list 参数不能为空')
        review_words = NewWord.objects.filter(word__in=word_list)
        for word_obj in review_words:
            review_word(word_obj)

        return Response('success')
