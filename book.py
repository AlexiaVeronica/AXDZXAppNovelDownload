import ahttp
import API
from instance import *


class Book:
    setup_config()

    def __init__(self, book_info: dict, index=None):
        self.index = index
        self.book_name = book_info.get('title')
        self.book_id = book_info.get('_id')
        self.author_name = book_info.get('author')
        self.book_intro = book_info.get('longIntro')
        self.book_state = book_info.get('zt')
        self.book_tag = book_info.get('cat')
        self.word_count = book_info.get('wordCount')
        self.book_updated = book_info.get('updated')
        self.last_chapter = book_info.get('lastChapter')

    def show_book_info(self) -> str:
        show_info = '书籍书名: {}\n'.format(self.book_name)
        show_info += '书籍作者: {}\n'.format(self.author_name)
        show_info += '书籍状态: {}\n'.format(self.book_state)
        show_info += '书籍字数: {}\n'.format(self.word_count)
        show_info += '更新时间: {}\n'.format(self.book_updated)
        show_info += '书籍标签: {}\n'.format(self.book_tag)
        show_info += '最新章节: {}\n'.format(self.last_chapter)
        print(show_info)
        return show_info

    def book_information(self):
        if self.last_chapter is not None:
            save_path = os.path.join(Vars.cfg.data.get('save_book'), self.book_name, f'{self.book_name}.txt')
            write(save_path, 'w', f'{self.show_book_info()}简介信息: {self.book_intro}\n')
        self.continue_chapter()

    def continue_chapter(self):
        filename_list = ''.join(os.listdir(os.path.join(Vars.cfg.data.get('config_book'), self.book_name)))
        download_chapter_list = [
            chapters.get('link') for chapters in API.Book.catalogue(self.book_id)
            if chapters.get('link').split('/')[1].rjust(4, "0") + '-' not in filename_list
        ]
        download_chapter_len = len(download_chapter_list)
        if download_chapter_len != 0 and download_chapter_list != []:
            chapter_dict = {
                'chapter_id': [API.Chapter.download_chapter(url) for url in download_chapter_list],
                'file_id': [url.split('/')[1] for url in download_chapter_list]
            }

            for page, data in enumerate(ahttp.run(chapter_dict['chapter_id'], pool=40, order=True)):
                chapter_title = del_title(data.json()['chapter']['title'])
                content = "\n\n\n{}\n\n{}".format(chapter_title, data.json()['chapter']['body'])
                filename = str(chapter_dict['file_id'][page]).rjust(4, "0") + '-' + chapter_title + '.txt'
                write(os.path.join(Vars.cfg.data.get('config_book'), self.book_name, filename), 'w', content)
                print('下载进度:{:^3.0f}%'.format((page / download_chapter_len) * 100), end='\r')

        file_name_list = os.listdir(os.path.join(Vars.cfg.data.get('config_book'), self.book_name))  # 获取文本名
        file_name_list.sort(key=lambda x: int(x.split('-')[0]))  # 按照数字顺序排序文本

        for file_name in file_name_list:  # 遍历文件名
            """遍历合并文本所在的路径的单个文件"""
            content = write(os.path.join(Vars.cfg.data.get('config_book'), self.book_name, file_name), 'r').read()
            Vars.epub_info.add_chapter(
                file_name.split('-')[1].replace('.txt', ''), content.replace('\n', '</p>\r\n<p>'),
                file_name.split('-')[0]
            )
            write(
                os.path.join(Vars.cfg.data.get('save_book'), self.book_name, f'{self.book_name}.txt'), 'a', content
            )
        Vars.epub_info.save()
        print(self.book_name, '本地档案合并完毕')
