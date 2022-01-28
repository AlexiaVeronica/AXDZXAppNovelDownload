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
            self.epub = epub.EpubFile(book_id, book_name, author_name)

            self.show_book_info(book_name, author_name, book_state, word_count, book_updated,
                                book_tag, last_chapter, book_intro)
            self.continue_chapter(book_name, book_id)

        else:
            print('输入的小说序号不存在！')

    def show_book_info(self, book_name, author_name, book_state, word_count,
                       book_updated, book_tag, last_chapter, book_intro):
        makedirs(self.path(Vars.cfg.data.get('config_book'), book_name))
        show_info = ''
        show_info += '书籍书名: {}\n'.format(book_name)
        show_info += '书籍作者: {}\n'.format(author_name)
        show_info += '书籍状态: {}\n'.format(book_state)
        show_info += '书籍字数: {}\n'.format(word_count)
        show_info += '更新时间: {}\n'.format(book_updated)
        show_info += '书籍标签: {}\n'.format(book_tag)
        show_info += '最新章节: {}\n'.format(last_chapter)
        print(show_info)

        mkdir(self.path(Vars.cfg.data.get('save_book'), book_name))
        save_path = self.path(Vars.cfg.data.get('save_book'), book_name, f'{book_name}.txt')
        write(save_path, 'w', f'{show_info}简介信息: {book_intro}\n')
        self.epub.add_intro(author_name, book_updated, last_chapter, book_intro, book_tag)

    def continue_chapter(self, book_name, book_id):
        """通过目录接口获取小说章节ID，并跳过已经存在的章节"""
        catalogue_list = self.catalogue.get('mixToc').get('chapters')
        save_urls_list = []
        filename_list = os.listdir(self.path(Vars.cfg.data.get('config_book'), book_name))
        for _list in catalogue_list:
            link = _list['link']
            if link.split('/')[1].rjust(4, "0") + '-' in ''.join(filename_list):
                continue
            save_urls_list.append(link)

        progress = len(save_urls_list)
        if progress == 0 or save_urls_list == []:
            print(f'小说 {book_name} 没有需要下载的章节')
        else:
            print('一共有{}章需要下载'.format(progress))
            with ThreadPoolExecutor(max_workers=Vars.cfg.data.get('Pool')) as executor:
                for progress_number, url in enumerate(save_urls_list):
                    file_number = url.split('/')[1]
                    executor.submit(self.download, book_name, url, file_number, progress_number, progress)
            print(f'小说 {book_name} 下载完成')
        self.out_file_dir(book_name)

    def out_file_dir(self, book_name):
        config_path = self.path(Vars.cfg.data.get('config_book'), book_name)
        save_book_path = self.path(Vars.cfg.data.get('save_book'), book_name, f'{book_name}.txt')
        filenames = os.listdir(config_path)  # 获取文本名
        filenames.sort(key=lambda x: int(x.split('-')[0]))  # 按照数字顺序排序文本
        file = write(save_book_path, 'a')

        """遍历文件名"""
        for filename in filenames:
            serial_number = filename.split('-')[0]
            chapter_title = filename.split('-')[1].replace('.txt', '')
            chapter_content = ''
            filepath = self.path(config_path, filename)  # 合并文本所在的路径
            """遍历单个文件，读取行数"""
            for content_line in open(filepath, encoding='UTF-8'):
                if '长按' or '在线观看' in '微信公众' or 'www' in content_line:
                    continue
                if '　　?' in content_line:
                    content_line = content_line.replace('　　?', '　　')
                chapter_content += f'\n<p>{content_line}</p>'
                file.writelines(content_line)
            file.write('\n')
            self.epub.add_chapter(chapter_title, chapter_content, serial_number)
        file.close()
        self.epub.save()

    def download(self, book_name, chapter_id, file_number, progress_number, progress):
        print(f'下载进度:{progress_number}/{progress}', end="\r")
        response = API.Chapter.download_chapter(chapter_id)

        chapter_title = del_title(response.get('chapter').get('title'))
        chapter_content = response.get('chapter').get('body')

        title_body = "\n\n\n{}\n\n{}".format(chapter_title, chapter_content)  # 标题加正文
        filename = str(file_number).rjust(4, "0") + '-' + chapter_title + '.txt'
        write(self.path(Vars.cfg.data.get('config_book'), book_name, filename), 'w', title_body)
        time.sleep(0.1)
        return '{}下载成功'.format(chapter_title)
