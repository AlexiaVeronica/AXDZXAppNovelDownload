import threading
import API
from instance import *


class Book:
    setup_config()

    def __init__(self, book_info: dict, index=None):
        self.index = index
        self.progress_bar = 1
        self.thread_list = list()
        self.pool_sema = threading.BoundedSemaphore(10)
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
        return '{}简介信息:\n {}'.format(show_info, self.book_intro)

    def book_information(self, config_dir: str, save_dir: str):
        if self.last_chapter is not None:
            write(save_dir + '/' + f'{self.book_name}.txt', 'w', self.show_book_info())
        if self.download_chapter_threading() == 0:
            print("没有需要下载的章节！")
        self.output_text_and_epub(config_dir, save_dir)
        print(self.book_name, '本地档案合并完毕')

    def progress(self, download_length):
        percentage = (self.progress_bar / download_length) * 100
        print('{}/{} 进度:{:^3.0f}%'.format(self.progress_bar, download_length, percentage), end='\r')
        self.progress_bar += 1

    def output_chapter_content(self, chapter_title, chapter_content):
        content = ""
        for line in chapter_content.splitlines():
            chapter_line = line.strip("　").strip()
            if chapter_line != "" or len(chapter_line) > 2:
                if "http" in chapter_line:
                    continue
                content += "\n　　{}".format(chapter_line)
        return f"{chapter_title}\n\n{content}"

    def download_content(self, chapter_url, file_id, download_length):
        self.pool_sema.acquire()
        chapter_title, chapter_content = API.Chapter.download_chapter(chapter_url)
        file_name = f"{file_id}-{del_title(chapter_title)}.txt"
        write(
            f"{Vars.cfg.data.get('config_book')}/{self.book_name}/{file_name}", 'w',
            self.output_chapter_content(chapter_title, chapter_content)
        )
        self.progress(download_length)
        self.pool_sema.release()

    def output_text_and_epub(self, config_dir, save_dir):
        file_name_list = os.listdir(config_dir)  # 获取目录文本名
        file_name_list.sort(key=lambda x: int(x.split('-')[0]))  # 按照数字顺序排序文本
        for file_name in file_name_list:  # 遍历文件名
            """遍历合并文本所在的路径的单个文件"""
            content = write(os.path.join(config_dir, file_name), 'r').read()
            chapter_index = file_name.split('-')[1].replace('.txt', '')
            Vars.epub_info.add_chapter(chapter_index, content, file_name.split('-')[0])
            write(f'{save_dir}/{self.book_name}.txt', 'a', "\n\n"+content)
        Vars.epub_info.save()

    def get_chapter_url(self):
        filename_list = os.listdir(os.path.join(Vars.cfg.data.get('config_book'), self.book_name))
        chapter_list = [
            chapters.get('link') for chapters in API.Book.catalogue(self.book_id)
            if chapters.get('link').split('/')[1].rjust(4, "0") + '-' not in ''.join(filename_list)
        ]
        return len(chapter_list), chapter_list

    def download_chapter_threading(self):
        download_length, download_chapter_list = self.get_chapter_url()
        if download_length == 0:
            return download_length
        file_id_list = [url.split('/')[1] for url in download_chapter_list]
        for index, chapter_url in enumerate(download_chapter_list):
            file_id = str(file_id_list[index]).rjust(4, "0")
            thread = threading.Thread(
                target=self.download_content, args=(chapter_url, file_id, download_length,)
            )
            self.thread_list.append(thread)

        for thread in self.thread_list:
            thread.start()

        for thread in self.thread_list:
            thread.join()
        self.thread_list.clear()
