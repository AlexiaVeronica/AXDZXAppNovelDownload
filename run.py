import src
import book
import epub
from instance import *


def agreed_read_readme():
    if Vars.cfg.data.get('agreed_to_readme') != 'yes':
        print(Msgs.msg_agree_terms)
        confirm = inputs_('>').strip()
        if confirm == 'yes' or confirm == '同意':
            Vars.cfg.data['agreed_to_readme'] = 'yes'
            Vars.cfg.save()
        else:
            sys.exit()


def shell_book(inputs: list):  # 通过小说ID下载单本小说
    if len(inputs) >= 2:
        Vars.book_info = src.Book.novel_info(inputs[1])
    else:
        raise Exception("you need input book id, please check your input")

    if Vars.book_info.get("_id") is not None:
        Vars.book_info = book.Book(Vars.book_info)
        Vars.epub_info = epub.EpubFile(
            Vars.book_info.book_id, Vars.book_info.book_name, Vars.book_info.author_name)
        Vars.epub_info.add_intro(
            Vars.book_info.author_name, Vars.book_info.book_updated, Vars.book_info.last_chapter,
            Vars.book_info.book_intro, Vars.book_info.book_tag
        )
        mkdir(Vars.cfg.data.get('save_book') + "/" + Vars.book_info.book_name)
        if os.path.exists(Vars.book_info.book_config):
            Vars.book_info.config_json = json.loads(open(Vars.book_info.book_config, 'r', encoding='utf-8').read())
        else:
            Vars.book_info.config_json = []

        print("开始下载《{}》\n{}".format(Vars.book_info.book_name, Vars.book_info.description))

        write(
            Vars.book_info.output_text, "w", '{}简介:\n{}'.format(Vars.book_info.description, Vars.book_info.book_intro)
        )
        Vars.book_info.start_downloading_novels()
    else:
        print("get book info error, the book id is not exist!")


def shell_search_book(inputs):
    if len(inputs) >= 2:
        start = time.time()
        response = src.Book.search_book(inputs[1]).get('books')
        for index, books in enumerate(response):
            shell_book([index, books.get('_id')])
        print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    else:
        print('未输入书名')


def get_pool(inputs):
    if len(inputs) >= 2:
        if inputs[1].isdigit():
            Vars.cfg.data['Thread_Pool'] = int(inputs[1])
            Vars.cfg.save(), print("线程已设置为", Vars.cfg.data.get('Thread_Pool'))
            return
        print("设置失败，输入信息不是数字")
    else:
        print("默认线程为", Vars.cfg.data.get('Thread_Pool'))


def shell_tag(inputs):
    if len(inputs) >= 2 and inputs[1].isdigit():
        tag_id = int(inputs[1])
        if Msgs.msg_tag.get(tag_id) is None:
            print(f"{tag_id} 标签号不存在\n")
            for key, Value in Msgs.msg_tag.items():
                print('{}:\t\t\t{}'.format(key, Value))
            return
        page = 0
        while True:
            tag_name = Msgs.msg_tag[tag_id]
            response = src.Tag.tag_info(inputs[1], tag_name, page).get("books")
            if response is None:
                break
            for index, tag_info_data in enumerate(response, start=1):
                print("\n\n{}分类 第{}本\n".format(tag_name, index))
                shell_book([index, tag_info_data.get('_id')])
            page += 20
    else:
        print(src.Tag.get_tag_type_information())


def shell_ranking(inputs):
    if len(inputs) >= 2:
        novel_list = []
        for data in src.Tag.ranking(inputs[1])['ranking']['books']:
            for key, Value in data.items():
                if key == 'title':
                    print('\n\n{}:\t\t\t{}'.format(key, Value))
                    continue
                book_info = '{}:\t\t\t{}'.format(key, Value) if len(
                    key) <= 6 else '{}:\t\t{}'.format(key, Value)
                print(book_info)
            novel_list.append(data.get('_id'))
        for index, novel_id in enumerate(novel_list):
            shell_book([index, novel_id])

    else:
        ranking_dict = {'周榜': '1', '月榜': '2', '总榜': '3'}
        for key, Value in ranking_dict.items():
            print('{}:\t\t\t{}'.format(key, Value))


def shell_list(inputs):
    start = time.time()
    list_file_name = inputs[1] + '.txt' if len(inputs) >= 2 else 'list.txt'
    try:
        list_file_input = open(list_file_name, 'r', encoding='utf-8')
        book_list = [line for line in list_file_input.readlines() if re.match("^\\s*([0-9]{1,7}).*$", line)]
        for book_id in book_list:
            shell_book(['', re.sub("^\\s*([0-9]{1,7}).*$\\n?", "\\1", book_id)])
        print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    except OSError:
        print(f"{list_file_name}文件不存在")


def shell():
    if len(sys.argv) > 1:
        command_line, inputs = True, sys.argv[1:]
    else:
        print('\n'.join(Msgs.msg_help))
        command_line, inputs = False, re.split('\\s+', inputs_('>').strip())
    while True:
        if inputs[0].startswith('q') or inputs[0] == '--quit':
            sys.exit("已退出程序")
        if inputs[0] == 'h' or inputs[0] == '--help':
            print('\n'.join(Msgs.msg_help))
        elif inputs[0] == 't' or inputs[0] == '--tag':
            shell_tag(inputs)
        elif inputs[0] == 'd' or inputs[0] == '--download':
            shell_book(inputs)
        elif inputs[0] == 'n' or inputs[0] == '--name':
            shell_search_book(inputs)
        elif inputs[0] == 'r' or inputs[0] == '--rank':
            shell_ranking(inputs)
        elif inputs[0] == 'u' or inputs[0] == '--update':
            shell_list(inputs)
        elif inputs[0] == 'p' or inputs[0] == '--pool':
            get_pool(inputs)
        else:
            print(inputs[0], '不是有效命令')
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', inputs_('>').strip())


if __name__ == '__main__':
    setup_config()
    agreed_read_readme()
    shell()
