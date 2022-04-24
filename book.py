import operator
import threading
import API
from instance import *


def output_chapter_content(chapter_content, chapter_title="", intro=False):
    content = ""
    if intro is True:
        for line in chapter_content.splitlines():
            chapter_line = line.strip("　").strip()
            if chapter_line != "":
                content += "\n" + chapter_line[:60]
        return content
    for line in chapter_content.splitlines():
        chapter_line = line.strip("　").strip()
        if chapter_line != "" and len(chapter_line) > 2:
            if "http" in chapter_line:
                continue
            content += "\n　　{}".format(chapter_line)
    return f"{chapter_title}\n\n{content}"


class Book:

    def __init__(self, book_info: dict, index=None):
        self.index = index
        self.progress_bar = 1
        self.config_json = []
        self.chapter_id_list = []
        self.thread_list = list()
        self.pool_sema = threading.BoundedSemaphore(32)
        self.book_name = book_info.get('title')
        self.book_id = book_info.get('_id')
        self.author_name = book_info.get('author')
        self.book_intro = book_info.get('longIntro')
        self.book_state = book_info.get('zt')
        self.book_tag = book_info.get('cat')
        self.word_count = book_info.get('wordCount')
        self.book_updated = book_info.get('updated')
        self.last_chapter = book_info.get('lastChapter')
        self.book_config = f"{Vars.cfg.data.get('config_book')}/{self.book_name}" + '.json'

    def show_book_info(self) -> str:
        show_info = '作者:{0:<{2}}状态:{1}\n'.format(self.author_name, self.book_state, isCN(self.author_name))
        show_info += '标签:{0:<{2}}字数:{1}\n'.format(self.book_tag, self.word_count, isCN(self.book_tag))
        show_info += '最新:{0:<{2}}更新:{1}\n'.format(self.last_chapter, self.book_updated, isCN(self.last_chapter))
        print(show_info)
        if not os.path.exists(self.book_config):
            open(self.book_config, "a").write("[]")
        self.config_json = json.loads(open(self.book_config, 'r', encoding='utf-8').read())
        return '{}简介:\n{}'.format(show_info, output_chapter_content(self.book_intro, intro=True))

    def download_book(self):
        save_dir = os.path.join(Vars.cfg.data.get('save_book'), self.book_name, f'{self.book_name}.txt')
        if self.last_chapter is not None:
            write(save_dir, 'w', self.show_book_info())
        chapter_list = self.get_chapter_url()
        if len(chapter_list) == 0:
            print("没有需要下载的章节！")
        else:
            self.download_chapter_threading(len(chapter_list), chapter_list)
            print('\n下载完成！')
        self.output_text_and_epub(save_dir)
        print(self.book_name, '本地档案合并完毕')

    def progress(self, download_length):
        percentage = (self.progress_bar / download_length) * 100
        print('{}/{} 进度:{:^3.0f}%'.format(self.progress_bar, download_length, percentage), end='\r')
        self.progress_bar += 1

    def download_content(self, chapter_url, chapter_index, download_length):
        self.pool_sema.acquire()
        chapter_title, chapter_content = API.Chapter.download_chapter(chapter_url)
        content_config = {
            'index': chapter_index,
            'title': chapter_title,
            'content': output_chapter_content(chapter_content, chapter_title),
        }
        self.config_json.append(content_config)
        self.progress(download_length)
        self.pool_sema.release()

    def output_text_and_epub(self, save_dir):
        self.config_json = sorted(self.config_json, key=lambda list1: int(list1["index"]))  # 按照数字顺序排序文本
        for config_info in self.config_json:  # 遍历文件名
            """遍历合并文本所在的路径的单个文件"""
            Vars.epub_info.add_chapter(config_info['title'], config_info['content'], config_info['index'])
        write(save_dir, 'a', ''.join(["\n\n\n" + config_info['content'] for config_info in self.config_json]))
        Vars.epub_info.save()
        self.config_json.clear()
        self.chapter_id_list.clear()

    def get_chapter_url(self):
        response = API.Book.catalogue(self.book_id)
        if response is None:
            return self.chapter_id_list
        config_tests = [chapters.get('title') for chapters in self.config_json]
        if len(self.config_json) == 0:
            link_list = [chapters.get('link') for chapters in response]
            return len(link_list), link_list
        for index, info in enumerate(response):
            if info['title'] in config_tests and info.get('content') != "":
                continue
            self.chapter_id_list.append(info['link'])

        return self.chapter_id_list

    def download_chapter_threading(self, download_length, chapter_list):
        if download_length == 0:
            return download_length
        for index, chapter_url in enumerate(chapter_list):
            chapter_index = chapter_url.split('/')[1]
            thread = threading.Thread(
                target=self.download_content, args=(chapter_url, chapter_index, download_length,)
            )
            self.thread_list.append(thread)

        for thread in self.thread_list:
            thread.start()

        for thread in self.thread_list:
            thread.join()
        self.thread_list.clear()
        with open(self.book_config, 'w', encoding='utf-8') as f:
            json.dump(self.config_json, f, indent=4, ensure_ascii=False)
