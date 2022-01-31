from concurrent.futures import ThreadPoolExecutor

import API
import epub
from API.Settings import *


class Book:
    setup_config()

    def __init__(self, book_id):
        self.epub = None
        self.path = os.path.join
        self.response = API.Book.novel_info(book_id)
        self.catalogue = API.Book.catalogue(book_id)
        self.save_book = Vars.cfg.data.get('save_book')
        self.config_book = Vars.cfg.data.get('config_book')

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
            mkdir(self.save_book)
            mkdir(self.config_book)
            self.epub = epub.EpubFile(book_id, book_name, author_name)

            self.show_book_info(book_name, author_name, book_state, word_count,
                                book_updated, book_tag, last_chapter, book_intro)
            self.continue_chapter(book_name)

        else:
            print('输入的小说序号不存在！')

    def show_book_info(
            self, book_name, author_name, book_state, word_count,
            book_updated, book_tag, last_chapter, book_intro
    ):
        makedirs(self.path(self.config_book, book_name))
        show_info = ''
        show_info += '书籍书名: {}\n'.format(book_name)
        show_info += '书籍作者: {}\n'.format(author_name)
        show_info += '书籍状态: {}\n'.format(book_state)
        show_info += '书籍字数: {}\n'.format(word_count)
        show_info += '更新时间: {}\n'.format(book_updated)
        show_info += '书籍标签: {}\n'.format(book_tag)
        show_info += '最新章节: {}\n'.format(last_chapter)
        print(show_info)

        mkdir(self.path(self.save_book, book_name))
        save_path = self.path(self.save_book, book_name, f'{book_name}.txt')
        write(save_path, 'w', f'{show_info}简介信息: {book_intro}\n')
        self.epub.add_intro(author_name, book_updated, last_chapter, book_intro, book_tag)

    def continue_chapter(self, book_name):
        """通过目录接口获取小说章节ID，并跳过已经存在的章节"""
        filename_list = ''.join(os.listdir(self.path(self.config_book, book_name)))
        chapters_url = self.catalogue.get('mixToc').get('chapters')
        if chapters_url is None:
            return '书籍信息获取失败'
        url_list = [
            chapters.get('link') for chapters in chapters_url
            if chapters.get('link').split('/')[1].rjust(4, "0") + '-' not in filename_list
        ]

        progress = len(url_list)
        with ThreadPoolExecutor(max_workers=Vars.cfg.data.get('Pool')) as executor:
            if progress != 0:
                print('一共有{}章需要下载'.format(progress))
            for progress_number, url in enumerate(url_list):
                file_number = url.split('/')[1]
                executor.submit(self.download, book_name, url, file_number, progress_number, progress)
        config_path = self.path(self.config_book, book_name)
        file_name_list = os.listdir(self.path(self.config_book, book_name))  # 获取文本名
        file_name_list.sort(key=lambda x: int(x.split('-')[0]))  # 按照数字顺序排序文本
        file = write(self.path(self.save_book, book_name, f'{book_name}.txt'), 'a')

        """遍历文件名"""
        for file_name in file_name_list:
            """遍历合并文本所在的路径的单个文件"""
            content = write(self.path(config_path, file_name), 'r').read()
            file.write(content)
            self.epub.add_chapter(
                file_name.split('-')[1].replace('.txt', ''), content.replace('\n', '</p>\r\n<p>'),
                file_name.split('-')[0]
            )
        file.close()
        self.epub.save()
        print(book_name, '本地档案合并完毕')

    def download(self, book_name, chapter_id, file_number, page, progress):
        response = API.Chapter.download_chapter(chapter_id)
        chapter_title = del_title(response.get('chapter').get('title'))
        chapter_content = response.get('chapter').get('body')
        title_body = "\n\n\n{}\n\n{}".format(chapter_title, chapter_content)  # 标题加正文
        filename = str(file_number).rjust(4, "0") + '-' + chapter_title + '.txt'
        write(self.path(self.config_book, book_name, filename), 'w', title_body)
        print('下载进度:{:^3.0f}%'.format((page / progress) * 100), end='\r')
        time.sleep(0.1)
