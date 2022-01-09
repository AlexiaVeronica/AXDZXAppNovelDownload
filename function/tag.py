import book
from function.instance import *
from API import UrlConstants, HttpUtil

class donwload_tag():
    def __init__(self, tag_id):
        self.page = 1
        self.tag_id = tag_id
        self.book_id_list = list()
        self.tag_api = UrlConstants.TAG_API
        self.tag_name = Vars.cfg.data.get('tag')[tag_id]

    def get_tag(self):
        print("开始下载 {}分类".format(self.tag_name))
        while True:
            self.page += 20
            tag_url = self.tag_api.format(self.tag_id, self.tag_name, self.page)
            response = HttpUtil.get(tag_url)
            if not response.get('books'):
                print("{} 分类下载完毕".format(self.tag_name))
                self.book_id_list.clear()
                break
            
            for data in response.get('books'):
                book_id = data.get('_id')
                self.book_id_list.append(book_id)
                print("开始下载第 {} 本\n".format(len(self.book_id_list)))
                book.Book(book_id).book_information()