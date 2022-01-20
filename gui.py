import PySimpleGUI as sg
import book
from API.Settings import *

setup_config()
Vars.cfg.load()


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
            novel_id = values['novel_id']
            if novel_id != '':
                book.Book(novel_id).book_information(types=False)
            else:
                sg.popup_timed('输入小说序号为空！', title='提醒')

        # if event == '_charcountbegin_':
        #     page = 0
        #     # print(values['_TagName_'])
        #     if values['_TagName_'] == '':
        #         values['_TagName_'] = '百合'
        #     tag_namber = Vars.cfg.data.get('tags_dict')[values['_TagName_']]
        #     # print(values['_update_'])
        #     if values['_update_'] == '':
        #         values['_update_'] = Vars.cfg.data.get("updatedays")
        #     get_day = str(values['_update_'])
        #     is_vip = Vars.cfg.data.get("novelvip")
        #     words_num = Vars.cfg.data.get('charcountbegin')
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

    window.close()


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
