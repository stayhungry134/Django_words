"""
name: book
create_time: 2024/1/19 15:44
author: Ethan

Description: 
"""
import os.path

import requests

from reading.models import Book, Chapter


class ShanbayBookSync:
    def __init__(self):
        self.headers = {
            'cookie': '_ga=GA1.2.1385338636.1703228181; sessionid="e30:1rQiQv:fpyB1lTCyt98rcm9jW6bN-8mq2Y"; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjU2MzMyNzcxLCJleHAiOjE3MDY1MTAzNDYsImV4cF92MiI6MTcwNjUxMDM0NiwiZGV2aWNlIjoiIiwidXNlcm5hbWUiOiJQaG9uZV9iMzkzODY3NGRiMWM5YzdlIiwiaXNfc3RhZmYiOjAsInNlc3Npb25faWQiOiJiZTdjYTZjNGI2OTQxMWVlODc3MTgyY2Q2ZWQxNjU0NiJ9.zm3IFJmQFXNvHWyudXB5HYGKbc0w_Zu3xoEbZ2uIOYY; csrftoken=c3e645e3238d79aeb9bde3d9556cc042; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22gvkuds%22%2C%22first_id%22%3A%2218c904f8c07e85-0ff459458d8d1b-26001951-1638720-18c904f8c081900%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218c904f8c07e85-0ff459458d8d1b-26001951-1638720-18c904f8c081900%22%7D; _gat=1',
            'origin': 'https://web.shanbay.com',
            'referer': 'https://web.shanbay.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

    def get_books(self):
        """
        获取书籍
        """
        import requests
        from reading.models import Book, Category
        books_url = 'https://apiv3.shanbay.com/reading/user/books'
        current_num = 0
        current_page = 1
        """
        初级（Beginner）： 表示适合初学者的难度，通常包括基础概念和简单的技能。
        中级（Intermediate）： 表示适合有一定经验的人，已经掌握了基础知识，并愿意深入学习更多高级概念和技能。
        高级（Advanced）： 表示适合有相当经验的人，已经熟练掌握了基础和中级的知识，并且能够处理更复杂、深奥的问题。
        精通（Mastery）
        """
        category = Category.objects.filter(key='book_beginner').first()
        if not category:
            category = Category(
                classify='book',
                key='book_beginner',
                name='初级'
            )
            category.save()

        while True:
            books_params = {
                'page': current_page,
                'ipp': 8
            }
            response = requests.get(books_url, params=books_params, headers=self.headers).json()
            objects = response['objects']
            for object in objects:
                book = object['book']
                if Book.objects.filter(third_id=book['book_id']).exists():
                    continue
                cover_name = self.get_book_cover(book['cover_urls'][0])
                book_obj = Book(
                    category=category,
                    title_cn=book['name_cn'],
                    title_en=book['name_en'],
                    cover=f'/reading/book/book_cover/{cover_name}',
                    third_id=book['book_id'],
                    description=book['description_cn'],
                    short_description=book['short_description'],
                    auther=object['authors'][0]['name_cn']
                )
                book_obj.save()
                print(f"{book['name_cn']}保存成功！")
            current_num += 8
            current_page += 1
            if current_num > response['total']:
                print('所有书籍同步完毕！')
                return

    def get_book_cover(self, url):
        import requests
        import uuid
        from django_words.settings import MEDIA_ROOT
        response = requests.get(url, headers=self.headers).content

        cover_path = os.path.join(MEDIA_ROOT, 'reading/book/book_cover')
        cover_name = f"{uuid.uuid4().hex}.jpg"
        with open(os.path.join(cover_path, cover_name), 'wb') as f:
            f.write(response)

        return cover_name

    def get_chapter(self, book_obj: Book):
        """
        获取书籍章节
        """
        from reading.models import Chapter
        chapter_url = f"https://apiv3.shanbay.com/reading/books/{book_obj.third_id}/catalogs"
        chapter_params = {
            'book_id': book_obj.third_id,
            'list_all': 'true'
        }
        if Chapter.objects.filter(book=book_obj).exists():
            print(f"{book_obj.title_cn}章节已存在！")
            return
        chapter_res = requests.get(chapter_url, params=chapter_params, headers=self.headers).json()
        catalogs = chapter_res['catalogs']
        for i, chapter in enumerate(catalogs):
            chapter_obj = Chapter(
                book=book_obj,
                index=i,
                title_cn=chapter['title_cn'],
                title_en=chapter['title_en'],
                third_id=chapter['id'],
                length=chapter['length']
            )
            chapter_obj.save()
            print(f"{chapter['title_cn']}保存成功！")

    def get_content(self, chapter_obj: Chapter):
        """
        获取章节内容
        """
        from reading.models import Content
        if Content.objects.filter(chapter=chapter_obj).exists():
            print(f"{chapter_obj.title_cn}内容已存在！")
            return
        content_url = f"https://apiv3.shanbay.com/reading/articles/{chapter_obj.third_id}/article_content"
        content_res = requests.get(content_url, headers=self.headers).json()
        content = []
        objects = content_res['objects']
        for object in objects:
            if 'img_url' in object.keys():
                content.append({
                    'type': 'image',
                    'img_url': object['img_url']
                })
            elif 'sentences' in object.keys():
                sentences = []
                for sentence in object['sentences']:
                    words = [word['item']['word'] for word in sentence['words']]
                    sentences.append(words)
                content.append({
                    'type': 'text',
                    'sentences': sentences
                })
        content_obj = Content(
            chapter=chapter_obj,
            content=content
        )
        content_obj.save()
        print(f"{chapter_obj.title_cn}内容保存成功！")



if __name__ == '__main__':
    book_sync = ShanbayBookSync()
    book_sync.get_books()
