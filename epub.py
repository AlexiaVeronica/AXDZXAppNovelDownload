from epub_novel import epub
from instance import *
import API


class EpubFile:
    def __init__(self, book_id, book_name, author_name):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.epub = epub.EpubBook()
        self.EpubList = list()
        self.path = os.path.join
        self.epub.set_language('zh-CN')
        self.epub.set_identifier(book_id)
        self.epub.set_title(book_name)
        self.epub.add_author(author_name)

    def add_intro(self, author_name, up_time, up_chapter, intro, novel_tag):
        intro_config = epub.EpubHtml(title='简介信息', file_name='0000-000000-intro.xhtml', lang='zh-CN')
        intro_html = """<html><head></head><body>\n<img src="./{}.png" alt="{}"/>\n<h1>简介</h1>
                        \n<p>书籍书名:{}</p>\n<p>书籍序号:{}</p>\n<p>书籍作者:{}</p>\n<p>更新时间:{}</p>
                        \n<p>最新章节:{}</p>\n<p>系统标签:{}</p>\n<p>简介信息:</p>\n{}</body></html> """
        intro_config.content = intro_html.format(
            self.book_name, "书籍封面", self.book_name, self.book_id, author_name, up_time, up_chapter, novel_tag, intro
        )
        self.epub.add_item(intro_config)
        self.EpubList.append(intro_config)
        self.epub.set_cover(self.book_name + '.png', API.Cover.download_cover())

    def add_chapter(self, chapter_title: str, content: str, serial_number: str):
        chapter_serial = epub.EpubHtml(
            title=chapter_title, file_name=str(serial_number).rjust(4, "0") + '.xhtml',
            lang='zh-CN', uid='chapter_{}'.format(serial_number)
        )

        chapter_serial.content = content.replace('\n', '</p>\r\n<p>')
        self.epub.add_item(chapter_serial)
        self.EpubList.append(chapter_serial)

    def save(self):
        self.epub.toc = tuple(self.EpubList)
        self.epub.spine = ['nav']
        self.epub.spine.extend(self.EpubList)
        self.epub.add_item(epub.EpubNcx())
        self.epub.add_item(epub.EpubNav())

        epub.write_epub(self.path(Vars.cfg.data.get('save_book'), self.book_name, self.book_name + '.epub'), self.epub,
                        {})
