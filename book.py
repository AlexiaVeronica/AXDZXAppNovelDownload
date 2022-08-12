import threading
import src
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
        self.download_length = 0
        self.index = index
        self.progress_bar = 1
        self.config_json = []
        self.chapter_id_list = []
        self.thread_list = list()
        self.book_info = book_info
        self.book_name = book_info.get('title')
        self.book_id = book_info.get('_id')
        self.author_name = book_info.get('author')
        self.book_state = book_info.get('zt')
        self.book_tag = book_info.get('cat')
        self.word_count = book_info.get('wordCount')
        self.book_updated = book_info.get('updated')
        self.last_chapter = book_info.get('lastChapter')
        self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data.get('max_threads'))

    @property
    def book_config(self):
        mkdir(Vars.cfg.data.get('config_book'))
        return f"{Vars.cfg.data.get('config_book')}/{self.book_name}" + '.json'

    @property
    def output_text(self):
        mkdir(os.path.join(Vars.cfg.data.get('save_book'), self.book_name))
        return os.path.join(Vars.cfg.data.get('save_book'), self.book_name, f'{self.book_name}.txt')

    @property
    def description(self) -> str:
        description_info = "书名:{}\n".format(self.book_name)
        description_info += "作者:{}\n".format(self.author_name)
        description_info += "标签:{}\n".format(self.book_tag)
        description_info += "状态:{}\n".format(self.book_state)
        description_info += "字数:{}\n".format(self.word_count)
        description_info += "最新:{}\n".format(self.last_chapter)
        description_info += "更新:{}\n".format(self.book_updated)
        return description_info

    @property
    def book_intro(self) -> str:
        return '\n'.join([i for i in self.book_info.get('longIntro').splitlines() if i.strip() != ""])

    def start_downloading_novels(self):
        if not os.path.exists(self.book_config):
            open(self.book_config, "a").write("[]")
        print(self.description)  # 打印书籍信息
        if self.last_chapter is not None:
            self.config_json = json.loads(open(self.book_config, 'r', encoding='utf-8').read())
            write(self.output_text, "w", '{}简介:\n{}'.format(self.description, self.book_intro))

        chapter_list = self.get_chapter_url()
        self.download_length = len(chapter_list)
        if self.download_length == 0:
            print("no need to download this book")
        else:
            self.download_chapter_threading(chapter_list)
            print('book download complete!')
        self.output_text_and_epub()
        print(self.book_name, '本地档案合并完毕')

    @property
    def progress_count(self):
        self.progress_bar += 1
        percentage = ((self.progress_bar / self.download_length) * 100)
        return '{}/{} percentage: {:^3.0f}%'.format(self.progress_bar, self.download_length, percentage)

    def thread_download_content(self, chapter_url, chapter_index):
        self.pool_sema.acquire()
        response = src.Book.download_chapter(chapter_url)
        content_text = [re.sub(r'\s+|　', '', i) for i in response['chapter']['body'].split('\n') if i.strip() != '']
        content_config = {
            'index': chapter_index,
            'title': response['chapter']['title'],
            'content': '\n　　'.join(content_text),
        }
        self.config_json.append(content_config)
        if Vars.cfg.data.get('real_time_cache'):
            with open(self.book_config, 'w', encoding='utf-8') as f:
                json.dump(self.config_json, f, ensure_ascii=False)
        print(self.progress_count, end='\r')
        self.pool_sema.release()

    def output_text_and_epub(self):
        self.config_json = sorted(self.config_json, key=lambda list1: int(list1["index"]))  # 按照数字顺序排序文本
        for config_info in self.config_json:  # 遍历文件名
            if config_info['content'] != "":  # 如果内容不为空
                Vars.epub_info.add_chapter(config_info['title'], config_info['content'], config_info['index'])
            else:
                print("{}章节内容为空！".format(config_info['title']))

        for config_info in self.config_json:
            write(self.output_text, 'a', "\n\n\n{}\n\n　　{}".format(config_info['title'], config_info['content']))
        Vars.epub_info.save()
        self.config_json.clear()
        self.chapter_id_list.clear()

    def get_chapter_url(self):
        response = src.Book.catalogue_info(self.book_id).get('mixToc').get('chapters')
        if isinstance(response, list) and len(response) > 0:
            if len(self.config_json) == 0:
                return [chapters.get('link') for chapters in response]
            for chapter_info in response:
                if chapter_info['title'] not in [i.get('title') for i in self.config_json]:
                    self.chapter_id_list.append(chapter_info['link'])
            else:
                print("{}".format(self.book_name), "本地缓存检测完毕！")
                if len(self.chapter_id_list) == 0:
                    print("全部章节已经是最新，没有需要下载的章节！")
                else:
                    print("一共{}章须下载！".format(len(self.chapter_id_list)))

        return self.chapter_id_list

    def download_chapter_threading(self, chapter_list):
        for index, chapter_url in enumerate(chapter_list):
            self.thread_list.append(threading.Thread(
                target=self.thread_download_content, args=(chapter_url, chapter_url.split('/')[1],)
            ))

        for thread in self.thread_list:
            thread.start()

        for thread in self.thread_list:
            thread.join()
        self.thread_list.clear()
        with open(self.book_config, 'w', encoding='utf-8') as f:
            json.dump(self.config_json, f, ensure_ascii=False, indent=4)
