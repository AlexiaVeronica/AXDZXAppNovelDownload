import API
import epub
from function.instance import *
from concurrent.futures import ThreadPoolExecutor


class Download:
    def __init__(self, book_name, book_id, author_name):
        self.path = os.path.join
        self.book_name = book_name
        self.book_id = book_id
        self.author_name = author_name
        self.epub = epub.EpubFile(book_id, book_name, author_name)

    def filedir(self):
        config_path = self.path(Vars.cfg.data.get('config_book'), self.book_name)
        save_book_path = self.path(Vars.cfg.data.get('save_book'), self.book_name, '{}.txt'.format(self.book_name))
        filenames = os.listdir(config_path)  # 获取文本名
        filenames.sort(key=lambda x: int(x.split('-')[0]))  # 按照数字顺序排序文本

        write(save_book_path, 'w')
        file = write(save_book_path, 'a')

        """遍历文件名"""
        for filename in filenames:
            serial_number = filename.split('-')[0]
            chapter_title = filename.split('-')[1].replace('.txt', '')
            chapter_content = ''
            filepath = self.path(config_path, filename)  # 合并文本所在的路径
            """遍历单个文件，读取行数"""
            for content_line in open(filepath, encoding='UTF-8'):
                if '长按' in content_line or '在线观看' in content_line or \
                        '微信公众' in content_line or 'www' in content_line:
                    continue
                if '　　?' in content_line:
                    content_line = content_line.replace('　　?', '　　')
                chapter_content += f'\n<p>{content_line}</p>'
                file.writelines(content_line)
            file.write('\n')
            self.epub.add_chapter(chapter_title, chapter_content, serial_number)
        file.close()
        self.epub.save()

    def download(self, chapter_id: str, file_number: int, progress_number: int, progress: int):
        print(f'下载进度:{progress_number}/{progress}', end="\r")

        response = API.Chapter.download_chapter(chapter_id)

        chapter_title = del_title(response.get('chapter').get('title'))
        chapter_content = response.get('chapter').get('body')

        title_body = "\n\n\n{}\n\n{}".format(chapter_title, chapter_content)  # 标题加正文
        filename = str(file_number).rjust(4, "0") + '-' + chapter_title + '.txt'
        write(self.path(Vars.cfg.data.get('config_book'), self.book_name, filename), 'w', title_body)
        time.sleep(0.1)
        return '{}下载成功'.format(chapter_title)

    def thread_pool(self, urls_list: list):
        progress = len(urls_list)
        if progress == 0:
            self.filedir()
            print(f'小说 {self.book_name} 没有需要下载的章节')
        else:
            print('一共有{}章需要下载'.format(progress))
            with ThreadPoolExecutor(max_workers=Vars.cfg.data.get('Pool')) as executor:
                for progress_number, url in enumerate(urls_list):
                    file_number = url.split('/')[1]
                    executor.submit(self.download, url, file_number, progress_number, progress)

            mkdir(self.path(Vars.cfg.data.get('save_book'), self.book_name))
            self.filedir()
            print(f'小说 {self.book_name} 下载完成')
