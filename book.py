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
            self.continue_chapter(book_name)

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

    def continue_chapter(self, book_name):
        """通过目录接口获取小说章节ID，并跳过已经存在的章节"""
        save_urls_list = []
        filename_list = os.listdir(self.path(Vars.cfg.data.get('config_book'), book_name))
        for _list in self.catalogue.get('mixToc').get('chapters'):
            link = _list['link']
            if link.split('/')[1].rjust(4, "0") + '-' in ''.join(filename_list):
                continue
            save_urls_list.append(link)

        progress = len(save_urls_list)
        if not save_urls_list or progress != 0:
            print('一共有{}章需要下载'.format(progress))
            with ThreadPoolExecutor(max_workers=Vars.cfg.data.get('Pool')) as executor:
                for progress_number, url in enumerate(save_urls_list):
                    file_number = url.split('/')[1]
                    executor.submit(
                        self.download, book_name, url, file_number, progress_number, progress
                    )

        self.out_file_dir(book_name)
        print(f'小说 {book_name} 本地档案合并完毕')

    def out_file_dir(self, book_name):
        config_path = self.path(Vars.cfg.data.get('config_book'), book_name)
        save_book_path = self.path(Vars.cfg.data.get('save_book'), book_name, f'{book_name}.txt')
        file_name_list = os.listdir(config_path)  # 获取文本名
        file_name_list.sort(key=lambda x: int(x.split('-')[0]))  # 按照数字顺序排序文本
        file = write(save_book_path, 'a')

        """遍历文件名"""
        for file_name in file_name_list:
            chapter_content = ''
            """遍历合并文本所在的路径的单个文件，读取行数"""
            for content_line in open(self.path(config_path, file_name), encoding='UTF-8'):
                file.writelines(content_line)
                chapter_content += f'\n<p>{content_line}</p>'
            self.epub.add_chapter(
                file_name.split('-')[1].replace('.txt', ''), chapter_content,
                file_name.split('-')[0]
            )
            file.write('\n')
        file.close()
        self.epub.save()

    def download(self, book_name, chapter_id, file_number, page, progress):
        print('下载进度:{:^3.0f}%'.format((page / progress) * 100), end='\r')

        response = API.Chapter.download_chapter(chapter_id)

        chapter_title = del_title(response.get('chapter').get('title'))
        chapter_content = response.get('chapter').get('body')

        title_body = "\n\n\n{}\n\n{}".format(chapter_title, chapter_content)  # 标题加正文
        filename = str(file_number).rjust(4, "0") + '-' + chapter_title + '.txt'
        write(self.path(Vars.cfg.data.get('config_book'), book_name, filename), 'w', title_body)
        time.sleep(0.1)
        return '{}下载成功'.format(chapter_title)
