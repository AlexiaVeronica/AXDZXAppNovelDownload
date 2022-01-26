import API
import book
from function.instance import *


class donwload_tag:
    def __init__(self, tag_id):
        self.page = 1
        self.tag_id = tag_id
        self.book_id_list = list()
        self.type_dict = {}
        self.tag_name = Vars.cfg.data.get('tag')[tag_id]

    def get_type(self):
        response = API.Tag.get_type()
        for number, sort in enumerate(response):
            print(sort)
            number += 1
            major = sort.get('major')
            self.type_dict[number] = major
        return self.type_dict

    def get_tag(self):
        print("开始下载 {}分类".format(self.tag_name))
        while True:
            self.page += 20
            response = API.Tag.tag_info(self.tag_id, self.tag_name, self.page)
            if not response.get('books'):
                print("{} 分类下载完毕".format(self.tag_name))
                self.book_id_list.clear()
                break

            for data in response.get('books'):
                book_id = data.get('_id')
                self.book_id_list.append(book_id)
                print("开始下载第 {} 本\n".format(len(self.book_id_list)))
                book.Book(book_id).book_information()
