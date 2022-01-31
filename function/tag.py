import ahttp
import API
import book
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

    def tag_information(self):

        response_list = [
            API.Tag.tag_info(self.tag_id, self.tag_name, i + 20) for i in range(5000)
        ]
        for result_data in ahttp.run(response_list):
            tag_info_list = result_data.json()['books']
            if tag_info_list and tag_info_list != []:
                for tag_info_data in tag_info_list:
                    novel_id = tag_info_data.get('_id')
                    self.book_id_list.append(novel_id)
                    print("\n\n{}分类 第{}本\n".format(self.tag_name, len(self.book_id_list)))
                    book.Book(novel_id).book_information()
            else:
                print("{} 分类下载完毕, 一共下载 {} 本".format(self.tag_name, self.book_id_list))
