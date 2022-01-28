import ahttp

import API
import book
from API import UrlConstants
from function.instance import *


class Tag:
    def __init__(self, tag_id):
        self.page = 1
        self.tag_id = tag_id
        self.book_id_list = list()
        self.type_dict = {}
        self.tag_name = Vars.cfg.data.get('tag')[tag_id]

    def get_type(self):
        for number, sort in enumerate(API.Tag.get_type()):
            print(sort)
            number += 1
            major = sort.get('major')
            self.type_dict[number] = major
        return self.type_dict

    def get_tag(self):
        print("开始下载 {}分类".format(self.tag_name))
        api_url_list = [UrlConstants.TAG_API.format(self.tag_id, self.tag_name, i + 20) \
                        for i in range(0, 10)]
        session = ahttp.Session()
        response = [session.get(api_url) for api_url in api_url_list]
        for number, result_data in enumerate(ahttp.run(response)):
            print('一共 {} 章, 下载进度:{:^3.0f}%'.format(
                len(response), (number / len(response)) * 100), end='\r')
            if not result_data.json()['books']:
                print("{} 分类下载完毕".format(self.tag_name))
                return
            for data in result_data.json().get('books'):
                book_id = data.get('_id')
                self.book_id_list.append(book_id)
                print("开始下载第 {} 本\n".format(len(self.book_id_list)))
                book.Book(book_id).book_information()
