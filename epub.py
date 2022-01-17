from ebooklib import epub
from function.instance import *
import API


class EpubFile:
    def __init__(self, book_id, book_name, author_name):
        self.epub = epub.EpubBook()
        self.book_name = book_name
        self.EpubList = list()
        self.path = os.path.join
        self.epub.set_language('zh-CN')
        self.epub.set_identifier(book_id)
        self.epub.set_title(book_name)
        self.epub.add_author(author_name)

    def cover(self):
        cover_url = API.Cover.get_cover()
        cover_path = API.Cover.download_cover(cover_url)
        self.epub.set_cover(self.book_name + '.png', cover_path)

    def add_chapter(self, chapter_title, chapter_content, serial_number):
        content = chapter_content
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
        # self.epub.add_item(default_css)
        chapter_serial = epub.EpubHtml(title=chapter_title, file_name='chapter_{}'.format(serial_number) + '.xhtml',
                                       lang='zh-CN', uid='chapter_{}'.format(serial_number))
        chapter_serial.content = content
        chapter_serial.add_item(default_css)
        self.epub.add_item(chapter_serial)
        self.EpubList.append(chapter_serial)

    def save(self):
        self.cover()
        self.epub.toc = tuple(self.EpubList)
        self.epub.spine = ['nav']
        self.epub.spine.extend(self.EpubList)
        self.epub.add_item(epub.EpubNcx())
        self.epub.add_item(epub.EpubNav())
        style = '''
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
                }
                '''
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.epub.add_item(nav_css)
        epub.write_epub(self.path(Vars.cfg.data.get('save_book'), self.book_name, self.book_name + '.epub'), self.epub, {})
