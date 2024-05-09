"""
name: 
create_time: 2024/5/9 16:10
author: Ethan

Description: 
"""
import yaml
import requests
import execjs

from celery import shared_task
from django_words.settings import BASE_DIR


@shared_task
def shanbay_word_list():
    """
    获取扇贝单词今日新词
    :return:
    """
    from word.utils import parse_data
    # 今日新词
    url = 'https://apiv3.shanbay.com/wordsapp/user_material_books/bhhua/learning/words/today_learning_items'
    params = {
        'ipp': 10,
        'page': 1,
        'type_of': 'NEW',
    }
    headers = {
        'Origin': 'https://web.shanbay.com',
        'Referer': 'https://web.shanbay.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    cookies = yaml.safe_load(open(f'{BASE_DIR}/config/shanbay_cookies.yaml', 'r', encoding='utf-8'))

    total_page = 5
    current_page = 1

    def get_learning_words(current_page=1, total_page=5):
        """
        获取已学单词
        :return:
        """
        res_words = {}
        while current_page <= total_page:
            params['page'] = current_page
            res = requests.get(url, params=params, headers=headers, cookies=cookies)
            res_json = res.json().get('data')
            word_json = parse_data(res_json)
            total = word_json.get('total')
            total_page = total // 10 + 1
            words = word_json.get('objects')
            words_list = [word_item['vocab_with_senses'] for word_item in words]
            words_dic = {word_item['word']: {'word': word_item['word'],
                                             'definition': [f"{definition['pos']} {definition['definition_cn']}" for
                                                            definition in word_item['senses']],
                                             'uk_audio': word_item['sound']['audio_uk_urls'][0],
                                             'us_audio': word_item['sound']['audio_us_urls'][0], }
                         for word_item in words_list}
            res_words.update(words_dic)
            current_page += 1
            print(f'已爬取第{current_page - 1}页')
        return res_words

    words_dic = get_learning_words(current_page, total_page)

    for word in words_dic.keys():
        requests.get('http://word.stayhungry134.com:8000/word_api/word/', params={'word': word})
