import PySimpleGUI as sg
import API, book, epub
from instance import *

setup_config()


def main():
    sg.theme('Default1')
    layout = [
        [sg.Menu([['选项', ['使用帮助', '免责声明']]])],
        [
            sg.T('书籍序号'), sg.Input(key='novel_id', size=(15, 1)),
            sg.B('下载', key='_downloader_', size=(5, 1))
        ],

    ]
    window = sg.Window('downloader', layout)
    while True:
        event, values = window.read()

        if event == '使用帮助':
            text = '使用帮助：\n'
            sg.popup_scrolled(text, title='使用帮助')

        if event == '免责声明':
            text = '本项目提供用于个人学习、研究或欣赏。通过使用项目随之而来的风险与作者无关'
            sg.popup(text, title='免责声明')

        if event == '_downloader_':
            if values['novel_id'] != '':
                Vars.book_info = API.Book.novel_info(values['novel_id'])
                if Vars.book_info is not None and isinstance(Vars.book_info, dict):
                    Vars.book_info = book.Book(Vars.book_info)
                    book_name = Vars.book_info.book_name
                    Vars.epub_info = epub.EpubFile(Vars.book_info.book_id, book_name, Vars.book_info.author_name)
                    Vars.epub_info.add_intro(
                        Vars.book_info.author_name, Vars.book_info.book_updated, Vars.book_info.last_chapter,
                        Vars.book_info.book_intro, Vars.book_info.book_tag
                    )
                    print("开始下载《{}》".format(book_name))
                    config_dir = Vars.cfg.data.get('config_book') + "/" + book_name
                    save_dir = Vars.cfg.data.get('save_book') + "/" + book_name
                    makedirs(config_dir), makedirs(save_dir)
                    Vars.book_info.download_book(config_dir, save_dir)
            else:
                sg.popup_timed('输入小说序号为空！', title='提醒')

    window.close()
        # if event == '_tag_':
        #         tag_id = inputs[1]
        #         if not Vars.cfg.data.get('tag').get(tag_id):
        #             print(f"{tag_id} 标签号不存在\n")
        #             for key, Value in Vars.cfg.data.get('tag').items():
        #                 print('{}:\t\t\t{}'.format(key, Value))
        #             return
        #         page = 0
        #         while True:
        #             tag_name = Vars.cfg.data.get('tag')[inputs[1]]
        #             response = API.Tag.tag_info(inputs[1], tag_name, page)
        #             if response is None: break
        #             for index, tag_info_data in enumerate(response, start=1):
        #                 print("\n\n{}分类 第{}本\n".format(tag_name, index))
        #                 shell_book([index, tag_info_data.get('_id')])
        #             page += 20
        #     else:
        #         print(API.Tag.get_type())
        #
        #     while True:
        #         response = BoluobaoAPI.Tag.tag_info(
        #             tag_namber, is_vip, get_day, words_num, page
        #         )
        #         page += 1
        #         if not response.get('data') or response.get('data') == []:
        #             print(f"已获取{values['_TagName_']}标签全部小说")
        #             break
        #         for data in response.get('data'):
        #             is_finish = '完结' if data.get('isFinish') else '未完'
        #
        #             # tb = pt.PrettyTable()
        #             # tb.field_names = Vars.cfg.data.get('info_list')
        #             show_ = [
        #                 data.get('novelName'),
        #                 data.get('authorName'),
        #                 data.get('signStatus'),
        #                 str(data.get('markCount')),
        #                 str(data.get('charCount')),
        #                 str(data.get('novelId')), is_finish,
        #                 data.get('lastUpdateTime')]
        #             # tb.add_row(show_)
        #
        #             # sg.Print('\t'.join(Vars.cfg.data.get('info_list')))
        #             sg.Print('\t'.join(show_))

        # time.sleep(100)


main()

# def Dark():
#     sg.theme('LigrhGray1')
#     layout = [[sg.Text('Theme Browser')],
#             [sg.Text('Click a Theme color to see demo window')],
#             [sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-LIST-', enable_events=True)],
#             [sg.Button('Exit')]]
#     window = sg.Window('Theme Browser', layout)

#     while True:  # Event Loop
#         event, values = window.read()
#         if event in (None, 'Exit'):
#             break
#         sg.theme(values['-LIST-'][0])
#         sg.popup_get_text('This is {}'.format(values['-LIST-'][0]))

#     window.close()
