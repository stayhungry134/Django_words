"""
name: magazine.py
create_time: 2024/1/11 10:47
author: Ethan

Description: 请求杂志相关的接口
"""
import os

import paramiko
import yaml
from django_words.settings import BASE_DIR


class MagazineSync:
    """
    杂志同步类
    """

    def __init__(self):
        yaml_path = os.path.join(BASE_DIR, 'reading/config/magazine.yaml')
        magazine_user = yaml.load(open(yaml_path, encoding='utf-8'), Loader=yaml.FullLoader)['magazine']
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(**magazine_user)
        self.sftp = self.ssh.open_sftp()

    def get_magazine_list(self):
        """
        检索杂志列表
        :return:
        """
        remote_root_path = '/magazine'
        magazine_dic = {}
        magazine_category_list = self.sftp.listdir(remote_root_path)
        for category in magazine_category_list:
            if category != '#recycle':
                magazine_dic[category] = []
                remote_magazine_category_path = f'{remote_root_path}/{category}'
                magazine_list = self.sftp.listdir(remote_magazine_category_path)
                for magazine in magazine_list:
                    remote_magazine_path = f'{remote_magazine_category_path}/{magazine}'
                    magazine_dic[category].append({
                        'name': magazine,
                        'path': remote_magazine_path
                    })
        return magazine_dic

    def sync(self):
        """
        同步杂志
        :return:
        """
        from reading.models import MagazineCategory, Magazine
        magazine_dic = self.get_magazine_list()
        for category, magazine_list in magazine_dic.items():
            category_obj = MagazineCategory.objects.filter(name=category).first()
            if not category_obj:
                category_obj = MagazineCategory(name=category)
                category_obj.save()
                # 如果之前没有这个分类，那么下面的所有杂志都需要重新同步
                new_magazines = []
                for magazine in magazine_list:
                    new_magazines.append(Magazine(name=magazine['name'],
                                                  category=category_obj,
                                                  path=magazine['path']))
                Magazine.objects.bulk_create(new_magazines)
            else:
                new_magazines = []
                exist_magazines = Magazine.objects.filter(category=category_obj).values_list('path', flat=True)
                for magazine in magazine_list:
                    if magazine['path'] not in exist_magazines:
                        new_magazines.append(Magazine(name=magazine['name'],
                                                      category=category_obj,
                                                      path=magazine['path']))
                Magazine.objects.bulk_create(new_magazines)

    def generate_cover(self):
        """
        生成杂志封面
        """
        from django.db.models import Q
        from reading.models import Magazine
        # 按需读取pdf第一页
        magazines = Magazine.objects.filter(Q(cover__isnull=True) | Q(cover='')).first()
        if not magazines:
            return
        cover_path = self.get_magazine_cover(magazines.path)
        magazines.cover = f"magazine/{cover_path}"
        magazines.save()

    def get_magazine_cover(self, remote_path):
        """
        获取杂志封面
        :param remote_path: 杂志远程路径
        :return:
        """
        import os
        from io import BytesIO
        from django_words.settings import MEDIA_ROOT
        import fitz
        chunk_size = 4096
        pdf_data = BytesIO()

        # 从 NAS 下载 pdf，分块读取
        with self.sftp.open(remote_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                pdf_data.write(chunk)

        # 读取 pdf 第一页
        pdf_data.seek(0)
        pdf = fitz.open(stream=pdf_data.read())
        first_page = pdf[0]
        image = first_page.get_pixmap()
        save_name = remote_path.replace('/', '_').replace(' ', '').replace('.pdf', '.jpg')
        save_path = os.path.join(MEDIA_ROOT, 'magazine', save_name)
        image.save(save_path)
        return save_name
