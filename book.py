import src
import threading
from instance import *


class Book:

    def __init__(self, book_info: dict):
        self.download_length = 0
        self.progress_bar = 1
        self._config_json = list()
        self.book_info = book_info
        self.book_name = book_info.get('title')
        self.book_id = book_info.get('_id')
        self.author_name = book_info.get('author')
        self.book_state = book_info.get('zt')
        self.book_tag = book_info.get('cat')
        self.word_count = book_info.get('wordCount')
        self.book_updated = book_info.get('updated')
        self.last_chapter = book_info.get('lastChapter')
        self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data['max_threads'])

    @property
    def config_json(self):
        return self._config_json

    @config_json.setter
    def config_json(self, value):
        if isinstance(value, dict):
            self._config_json.append(value)
        elif isinstance(value, list):
            self._config_json = value
        else:
            raise TypeError("config json must be dict or list, but {}".format(type(value)))

    @config_json.deleter
    def config_json(self):
        self._config_json.clear()

    @property
    def book_config(self) -> str:
        return os.path.join(mkdir(Vars.cfg.data.get('config_book')), self.book_name + '.json')

    @property
    def output_text(self) -> str:
        return os.path.join(mkdir(os.path.join(Vars.cfg.data['save_book'], self.book_name)), f'{self.book_name}.txt')

    @property
    def description(self) -> str:
        description_info = "书名:{}\n作者:{}\n".format(self.book_name, self.author_name)
        description_info += "标签:{}\n状态:{}\n".format(self.book_tag, self.book_state)
        description_info += "字数:{}\n最新:{}\n更新:{}\n".format(self.word_count, self.last_chapter, self.book_updated)
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

        self.get_chapter_url()
        self.download_length = len(Vars.current_catalogue.chapter_id_list)
        if self.download_length == 0:
            print("no need to download this book")
        else:
            self.download_chapter_threading()
            print('book download complete!')
        self.output_text_and_epub()
        print(self.book_name, '本地档案合并完毕')

    @property
    def progress_count(self):
        self.progress_bar += 1
        percentage = ((self.progress_bar / self.download_length) * 100)
        return '{}/{} percentage: {:^3.0f}%'.format(self.progress_bar, self.download_length, percentage)

    def set_content(self, chapter_url, chapter_index):
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
        del self.config_json

    def get_chapter_url(self):
        Vars.current_catalogue = Catalogue(src.Book.catalogue_info(self.book_id).get('mixToc'))
        if Vars.current_catalogue.chapter_count > 0:
            if len(self.config_json) == 0:
                Vars.current_catalogue.chapter_id_list = Vars.current_catalogue.chapters_url_list
            else:
                for chapter_info in Vars.current_catalogue.chapters_info_list:
                    if not Catalogue.test_local_chapter(chapter_info.get('title'), self.config_json):
                        Vars.current_catalogue.chapter_id_list = chapter_info['link']
                else:
                    print("{}".format(self.book_name), "本地缓存检测完毕！")
                    if len(Vars.current_catalogue.chapter_id_list) == 0:
                        print("全部章节已经是最新，没有需要下载的章节！")
                    else:
                        print("一共{}章须下载！".format(len(Vars.current_catalogue.chapter_id_list)))

    def download_chapter_threading(self):
        mult_thread_list = []
        for chapter_url in Vars.current_catalogue.chapter_id_list:
            mult_thread_list.append(
                threading.Thread(target=self.set_content, args=(chapter_url, chapter_url.split('/')[1],))
            )  # establish a thread for each chapter to download

        for thread in mult_thread_list:  # start threads one by one
            thread.start()

        for thread in mult_thread_list:  # wait for all threads to finish
            thread.join()

        mult_thread_list.clear()
        Vars.current_catalogue.chapter_id_list.clear()
        with open(self.book_config, 'w', encoding='utf-8') as f:
            json.dump(self.config_json, f, ensure_ascii=False, indent=4)


class Catalogue:
    def __init__(self, catalogue_info: dict):
        self._chapter_id_list = []
        self.catalogue_info = catalogue_info
        self.chapter_count = int(catalogue_info.get('chaptercount'))
        self.chapters_info_list = catalogue_info.get('chapters')
        self.chapters_updated = self.catalogue_info.get('chaptersUpdated')

    @property
    def chapters_url_list(self) -> list:
        return [chapters.get('link') for chapters in self.chapters_info_list]

    @property
    def chapters_title_list(self) -> list:
        return [chapters.get('title') for chapters in self.chapters_info_list]

    @staticmethod
    def test_local_chapter(chapter_title: str, local_chapter_list: list) -> bool:
        return any(chapter_title == local_info['title'] for local_info in local_chapter_list)

    @property
    def chapter_id_list(self):
        return self._chapter_id_list

    @chapter_id_list.setter
    def chapter_id_list(self, chapter_id: [str, list]):
        if isinstance(chapter_id, str):
            self._chapter_id_list.append(chapter_id)
        elif isinstance(chapter_id, list):
            self._chapter_id_list = chapter_id
