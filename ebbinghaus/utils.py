"""
name: utils
create_time: 2023/5/9
author: stayh

Description: 
"""
import requests


# 请求单词读音
def get_word_pronunciation(word):
    url = "http://dict.youdao.com/dictvoice"
    american_response = requests.get(url=url, params={'type': 0, 'audio': word})
    englishi_response = requests.get(url=url, params={'type': 0, 'audio': word})
