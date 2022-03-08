from instance import *
from ebook.ebooklib import epub
import API

Vars.epub_config = epub.EpubBook()


class EpubFile:

    def __init__(self):
        self.EpubList = list()
        self.path = os.path.join
        Vars.epub_config.set_language('zh-CN')
        Vars.epub_config.set_identifier(Vars.book_info.book_id)
        Vars.epub_config.set_title(Vars.book_info.book_name)
        Vars.epub_config.add_author(Vars.book_info.author_name)

    def add_intro(self):
        intro_ = epub.EpubHtml(title='简介信息', file_name='0000-000000-intro.xhtml', lang='zh-CN')
        intro_.content = '<html><head></head><body><h1>简介</h1>'
        intro_.content += '<p>书籍书名:{}</p><p>书籍序号:{}</p>'.format(Vars.book_info.book_name, Vars.book_info.book_id)
        intro_.content += '<p>书籍作者:{}</p><p>更新时间:{}</p>'.format(Vars.book_info.author_name, Vars.book_info.book_updated)
        intro_.content += '<p>最新章节:{}</p><p>系统标签:{}</p>'.format(Vars.book_info.last_chapter, Vars.book_info.book_tag)
        intro_.content += '<p>简介信息:</p>{}</body></html>'.format(Vars.book_info.book_intro)
        Vars.epub_config.add_item(intro_)
        self.EpubList.append(intro_)

    def cover(self):
        Vars.epub_config.set_cover(Vars.book_info.book_name + '.png', API.Cover.download_cover())

    def add_chapter(self, chapter_title: str, content: str, serial_number: str):
        default_style = '''
        body {font-size:100%;}
        p{
            font-family: Auto;
            text-indent: 2em;
        }
        h1{
            font-style: normal;
            font-size: 20px;
            font-family: Auto;
        }      
        '''
        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
                                    content=default_style)

        chapter_serial = epub.EpubHtml(
            title=chapter_title, file_name=str(serial_number).rjust(4, "0") + '-' + chapter_title + '.xhtml',
            lang='zh-CN', uid='chapter_{}'.format(serial_number)
        )

        chapter_serial.content = content
        chapter_serial.add_item(default_css)
        Vars.epub_config.add_item(chapter_serial)
        self.EpubList.append(chapter_serial)

    def save(self):
        self.cover()
        Vars.epub_config.toc = tuple(self.EpubList)
        Vars.epub_config.spine = ['nav']
        Vars.epub_config.spine.extend(self.EpubList)
        Vars.epub_config.add_item(epub.EpubNcx())
        Vars.epub_config.add_item(epub.EpubNav())
        style = """
                body {
                    font-family: Auto;
                }
                p{
                     font-family: Auto;
                     text-indent: 2em;
                }
                h2 {
                     text-align: left;
                     text-transform: uppercase;
                     font-weight: 200;     
                }
                ol {
                        list-style-type: none;
                }
                ol > li:first-child {
                        margin-top: 0.3em;
                }
                nav[epub|type~='toc'] > ol > li > ol  {
                    list-style-type:square;
                }
                nav[epub|type~='toc'] > ol > li > ol > li {
                        margin-top: 0.3em;
                }"""
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        Vars.epub_config.add_item(nav_css)
        epub.write_epub(
            self.path(Vars.cfg.data.get('save_book'), Vars.book_info.book_name, Vars.book_info.book_name + '.epub'),
                        Vars.epub_config, {})
