"""
name: utils
create_time: 2023/5/9
author: stayh

Description: 
"""
import requests


def get_word_translation(word):
    """请求单词翻译"""
    import sys
    import uuid
    import hashlib
    import time
    from importlib import reload
    reload(sys)
    headers = {
        'Referer': 'https: // dict.youdao.com / result?word = king & lang = en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    url = "https://dict.youdao.com/suggest"

    params = {
        'num': '5',
        'ver': '3.0',
        'doctype': 'json',
        'cache': 'false',
        'q': word,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json().get('result')
        if result.get('code') == 200:
            return response.json().get('data')
    else:
        return "查询失败了！"


print(get_word_translation('bloc'))



response = {
    "returnPhrase":["bloc"],
    # 源语言
    "query":"bloc",
    # 错误码
    "errorCode":"0",
    # 源语言目标语言
    "l":"en2zh-CHS",
    # 发音地址
    "tSpeakUrl":"https://openapi.youdao.com/ttsapi?q=%E9%9B%86%E5%9B%A2&langType=zh-CHS&sign=350221E23B25648915DC9EF3251ED74A&salt=1683788349727&voice=4&format=mp3&appKey=7ace14a1098eb019&ttsVoiceStrict=false",
    # 词义
    "web":[{"value":["集团", "国家集团", "团体"], "key":"bloc"},{"value":["东欧集团", "方集"], "key":"Eastern Bloc"},{"value":["魁人政团", "魁人党"], "key":"Bloc Québécois"}],
    "requestId":"6d299571-83ad-453a-abcf-22ce76952be5",
    # 翻译结果
    "translation":["集团"],
    "mTerminalDict":{"url":"https://m.youdao.com/m/result?lang=en&word=bloc"},
    "dict":{"url":"yddict://m.youdao.com/dict?le=eng&q=bloc"},
    "webdict":{"url":"http://mobile.youdao.com/dict?le=eng&q=bloc"},
    "basic":{"exam_type":["CET6", "GMAT"], "us-phonetic":"blɑːk", "phonetic":"blɒk", "uk-phonetic":"blɒk", "wfs":[{"wf":{"name":"复数", "value":"blocs"}}], "uk-speech":"https://openapi.youdao.com/ttsapi?q=bloc&langType=en&sign=285C079411D980B76FC1D7272FA74931&salt=1683788349727&voice=5&format=mp3&appKey=7ace14a1098eb019&ttsVoiceStrict=false", "explains":["n. 集团，阵营", "【名】 （Bloc）（法、罗）布洛克（人名）"], "us-speech":"https://openapi.youdao.com/ttsapi?q=bloc&langType=en&sign=285C079411D980B76FC1D7272FA74931&salt=1683788349727&voice=6&format=mp3&appKey=7ace14a1098eb019&ttsVoiceStrict=false"},
    "isWord":True,
    # 源语言发音地址
    "speakUrl":"https://openapi.youdao.com/ttsapi?q=bloc&langType=en-USA&sign=285C079411D980B76FC1D7272FA74931&salt=1683788349727&voice=4&format=mp3&appKey=7ace14a1098eb019&ttsVoiceStrict=false"}

