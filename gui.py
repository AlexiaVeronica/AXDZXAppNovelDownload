import threading
import PySimpleGUI as sg
import API
import book
import epub
from instance import *

setup_config()


def download_book():
    book_name = Vars.book_info.book_name
    Vars.epub_info = epub.EpubFile(Vars.book_info.book_id, book_name, Vars.book_info.author_name)
    Vars.epub_info.add_intro(
        Vars.book_info.author_name, Vars.book_info.book_updated, Vars.book_info.last_chapter,
        Vars.book_info.book_intro, Vars.book_info.book_tag
    )
    Vars.book_info.download_book()


def download_tag(tag_id):
    if not Msgs.msg_tag.get(tag_id):
        print(f"{tag_id} 标签号不存在\n")
        for key, Value in Msgs.msg_tag.items():
            print('{}:\t\t\t{}'.format(key, Value))
        return
    page = 0
    while True:
        tag_name = Msgs.msg_tag[tag_id]
        response = API.Tag.tag_info(tag_id, tag_name, page)
        if response is None: break
        for index, tag_info_data in enumerate(response, start=1):
            print("\n\n{}分类 第{}本\n".format(tag_name, index))
            Vars.book_info = API.Book.novel_info(tag_info_data['_id'])
            if Vars.book_info is not None and isinstance(Vars.book_info, dict):
                Vars.book_info = book.Book(Vars.book_info)
                print('开始下载{}'.format(Vars.book_info.book_name))
                download_book()
            else:
                print("获取失败")
        page += 20


def main():
    sg.theme('Default1')

    layout = [
        [sg.Menu([['选项', ['使用帮助', '免责声明']]])],
        [sg.Text('book id'), sg.InputText(key='-BID-', size=(25, 1))],
        [sg.Text('tags id'), sg.InputText(key='-TID-', size=(25, 1))],
        [sg.B('download', key="_DOWNLOAD_"), sg.B('tag', key="_TAG_"), sg.Button('exit')]]

    window = sg.Window('Window Title', layout, finalize=True)
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '使用帮助':
            text = '使用帮助：\n'
            sg.popup_scrolled(text, title='使用帮助')

        elif event == '免责声明':
            text = '本项目提供用于个人学习、研究或欣赏。通过使用项目随之而来的风险与作者无关'
            sg.popup(text, title='免责声明')

        elif event == "_DOWNLOAD_":
            print(values['-BID-'])
            if values['-BID-'] != "":
                Vars.book_info = API.Book.novel_info(values['-BID-'])
                if Vars.book_info is not None and isinstance(Vars.book_info, dict):
                    Vars.book_info = book.Book(Vars.book_info)
                    sg.popup_cancel('开始下载{}'.format(Vars.book_info.book_name))
                    threading.Thread(target=download_book).start()
                else:
                    print("获取失败")
            else:
                sg.popup_ok('获取书籍信息失败！', title='提醒')
        elif event == '_TAG_':
            if values['-TID-'] != "":
                threading.Thread(target=download_tag, args=(values['-TID-'],)).start()
            else:
                print("没有输入标签序号")
    window.close()


if __name__ == '__main__':
    main()
