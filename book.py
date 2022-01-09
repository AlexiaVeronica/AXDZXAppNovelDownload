from API import HttpUtil, api, UrlConstants
from API.Settings import *


class Book:
    setup_config()

    def __init__(self, book_id):
        self.path = os.path.join
        self.novel_api = UrlConstants.BOOK_INFO_API
        self.catalogue_api = UrlConstants.BOOK_CATALOGUE
        self.response = HttpUtil.get(self.novel_api.format(book_id))
        self.response_catalogue = HttpUtil.get(self.catalogue_api.format(book_id))
        mkdir(Vars.cfg.data.get('save_book'))
        mkdir(Vars.cfg.data.get('config_book'))

    def book_information(self):
        if self.response.get('_id'):
            book_name = self.response.get('title')
            book_id = self.response.get('_id')
            author_name = self.response.get('author')
            book_intro = self.response.get('longIntro')
            book_state = self.response.get('zt')
            book_tag = self.response.get('cat')
            word_count = self.response.get('wordCount')
            book_updated = self.response.get('updated')
            last_chapter = self.response.get('lastChapter')

            self.show_book_info(book_name, author_name, book_state, word_count, book_updated,
                                book_tag, last_chapter, book_intro)
            self.continue_chapter(book_name, book_id, author_name)

        else:
            print('输入的小说序号不存在！')

    def show_book_info(self, book_name, author_name, book_state, word_count,
                       book_updated, book_tag, last_chapter, book_intro):
        makedirs(self.path(Vars.cfg.data.get('config_book'), book_name))
        show_info = ''
        show_info += '书名: {}\n'.format(book_name)
        show_info += '作者: {}\n'.format(author_name)
        show_info += '状态: {}\n'.format(book_state)
        show_info += '字数: {}\n'.format(word_count)
        show_info += '更新: {}\n'.format(book_updated)
        show_info += '标签: {}\n'.format(book_tag)
        show_info += '更新: {}\n'.format(last_chapter)
        print(show_info)
        show_info += '简介信息: {}\n'.format(book_intro)

        """保存小说简介到配置文件"""
        write(self.path(Vars.cfg.data.get('config_book'), book_name, "0000-简介信息.txt"), 'w', show_info)

    def continue_chapter(self, book_name, book_id, author_name):
        """通过目录接口获取小说章节ID，并跳过已经存在的章节"""
        catalogue_list = self.response_catalogue.get('mixToc').get('chapters')
        save_urls_list = []
        filename_list = os.listdir(self.path(Vars.cfg.data.get('config_book'), book_name))
        for _list in catalogue_list:
            link = _list['link']
            if link.split('/')[1].rjust(4, "0") + '-' in ''.join(filename_list):
                continue
            save_urls_list.append(link)
        download = api.Download(book_name, book_id, author_name)
        download.thread_pool(save_urls_list)
