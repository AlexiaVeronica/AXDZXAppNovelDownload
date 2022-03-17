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
    config_dir = Vars.cfg.data.get('config_book') + "/" + book_name
    save_dir = Vars.cfg.data.get('save_book') + "/" + book_name
    makedirs(config_dir), makedirs(save_dir)
    Vars.book_info.download_book(config_dir, save_dir)


def main():
    sg.theme('Default1')

    layout = [
        [sg.Menu([['选项', ['使用帮助', '免责声明']]])],
        [sg.T('输入书籍序号')],
        [sg.Input(key='-BID-', size=(30, 1))],
        [sg.B('开始下载'), sg.Button('Exit')]]

    window = sg.Window('Window Title', layout, finalize=True)
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == '使用帮助':
            text = '使用帮助：\n'
            sg.popup_scrolled(text, title='使用帮助')

        if event == '免责声明':
            text = '本项目提供用于个人学习、研究或欣赏。通过使用项目随之而来的风险与作者无关'
            sg.popup(text, title='免责声明')

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "开始下载":
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
        # if event == '_DOWN_':
        #     if values['-BID-'] == "":
        #         sg.popup_ok('获取书籍信息失败！', title='提醒')
        #     else:
        #         print("执行")
    window.close()


if __name__ == '__main__':
    main()
