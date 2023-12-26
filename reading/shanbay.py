"""
name: shanbay
create_time: 2023/12/26 16:31
author: Ethan

Description: 请求扇贝数据的一些方法
"""
import logging
import os

import requests
import yaml
from django.db.models import Q

from django_words.settings import BASE_DIR


class Article:
    """
    请求文章的类
    """

    def __init__(self):
        self.cookies = self.get_cookies()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://web.shanbay.com/",
            "Origin": "https://web.shanbay.com",
        }

    def get_cookies(self):
        """
        获取cookie
        :return:
        """
        file_path = os.path.join(BASE_DIR, "reading/shanbay.yaml")
        file = open(file_path, encoding='utf-8')
        data = yaml.load(file, Loader=yaml.FullLoader)
        return data['cookies']

    def get_article_list(self):
        """
        获取文章列表
        :return:
        """
        from reading.models import Category, Article
        url = "https://apiv3.shanbay.com/news/retrieve/articles"
        page = 1
        total_page = 10
        while page < total_page:
            params = {
                "ipp": 10,
                "page": page
            }
            response = requests.get(url, params=params, cookies=self.cookies, headers=self.headers)
            if response.status_code != 200:
                raise Exception(f"请求失败--{response.json()}")
            data = response.json()
            total_page = data['total'] // 10 + 1
            articles = data['objects']
            print(f"第{page}页，共{total_page}页")
            for article in articles:
                category = article['category']
                category_obj = Category.objects.filter(key=category['id']).first()
                if not category_obj:
                    category_obj = Category.objects.create(key=category['id'], name=category['name'])
                    category_obj.save()
                article_obj = Article.objects.filter(third_key=article['id']).first()
                if not article_obj:
                    article_obj = Article.objects.create(
                        title_cn=article['title_cn'],
                        title_en=article['title_en'],
                        summary=article['summary'],
                        third_key=article['id'],
                        category=category_obj,
                        source='shanbay',
                        length=article['length']
                    )
                    article_obj.save()
            page += 1

    def get_article_content(self):
        """
        获取文章内容
        :return:
        """
        import xmltodict

        from reading.models import Article
        no_content_article = Article.objects.filter(Q(content__isnull=True) | Q(content__exact='')).first()
        if not no_content_article:
            logging.info("没有需要获取内容的文章")
            return
        url = f"https://apiv3.shanbay.com/news/articles/{no_content_article.third_key}?source=1"
        response = requests.get(url, cookies=self.cookies, headers=self.headers).json()
        article = response['content']
        dict_article = xmltodict.parse(article)['article_content']
        para = dict_article['para']

        content = []
        img_url = ''
        for paragraph in para:
            if 'img' in paragraph:
                img = paragraph['img']
                if isinstance(img, dict):
                    img_url = img['url']
            if 'sent' in paragraph:
                sent = paragraph['sent']
                if isinstance(sent, list):
                    for sentence in sent:
                        if isinstance(sentence, dict):
                            sentence['#text'] = sentence['#text'].replace('\n', '')
                        else:
                            sentence = sentence.replace('\n', '')
                        content.append(sentence)
                else:
                    sent['#text'] = sent['#text'].replace('\n', '')
            # 增加段落标记
            content.append('\n')

        # 保存图片
        if img_url:
            img_name = img_url.split('/')[-1]
            img_path = os.path.join(BASE_DIR, 'media/article', img_name)
            if not os.path.exists(img_path):
                img_response = requests.get(img_url, cookies=self.cookies, headers=self.headers)
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
            no_content_article.image = img_path

        # 保存文章内容
        content = ''.join(content)
        no_content_article.content = content
