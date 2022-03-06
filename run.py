import API
import book
from function.instance import *


def agreed_read_readme():
    if Vars.cfg.data.get('agreed_to_readme') != 'yes':
        print(Vars.cfg.data.get('agree_terms'))
        confirm = inputs_('>').strip()
        if confirm == 'yes' or confirm == '同意':
            Vars.cfg.data['agreed_to_readme'] = 'yes'
            Vars.cfg.save()
        else:
            sys.exit()


def shell_book(inputs):
    """通过小说ID下载单本小说"""
    if len(inputs) >= 2:
        response = API.Book.novel_info(inputs[1])
        if response:
            Vars.book_info = book.Book(response)
            Vars.book_info.book_information()
        else:
            print("获取书籍信息失败，请检查id或者重新尝试！")
    else:
        print('未输入Bookid')



def shell_search_book(inputs):
    """搜索书名下载小说"""
    if len(inputs) >= 2:
        start = time.time()
        response = API.Book.search_book(inputs[1])
        for index, books in enumerate(response):
            shell_book([index, books.get('_id')])
        print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    else:
        print('未输入书名')


def get_pool(inputs):
    if len(inputs) >= 2:
        if inputs[1].isdigit():
            Vars.cfg.data['Thread_Pool'] = int(inputs[1])
            Vars.cfg.save()
            print("线程已设置为", Vars.cfg.data.get('Thread_Pool'))

        else:
            print("设置失败，输入信息不是数字")
    else:
        print("默认线程为", Vars.cfg.data.get('Thread_Pool'))


def shell_tag(inputs):
    page = 0
    book_id_list = list()
    if len(inputs) >= 2:
        tag_id = inputs[1]
        if not Vars.cfg.data.get('tag').get(tag_id):
            print(f"{tag_id} 标签号不存在\n", Vars.cfg.data.get('tag'))
            print(API.Tag.get_type())
            return
        while True:
            tag_name = Vars.cfg.data.get('tag')[inputs[1]]
            response = API.Tag.tag_info(inputs[1], tag_name, page)
            if response is None:
                print("分类下载完毕, 一共下载 {} 本".format(book_id_list))
                break
            for index, tag_info_data in enumerate(response):
                novel_id = tag_info_data.get('_id')
                book_id_list.append(novel_id)
                print("\n\n{}分类 第{}本\n".format(tag_name, len(book_id_list)))
                shell_book([index, novel_id])
            page += 20
    else:
        print(API.Tag.get_type())


def shell_ranking(inputs):
    if len(inputs) >= 2:
        ranking_num = inputs[1]
        novel_list = []
        for data in API.Tag.ranking(ranking_num)['ranking']['books']:
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
    except OSError:
        print(f"{list_file_name}文件不存在")
        return
    for line in list_file_input.readlines():
        if re.match("^\\s*([0-9]{1,7}).*$", line):
            start = time.time()
            book_id = re.sub("^\\s*([0-9]{1,7}).*$\\n?", "\\1", line)
            book.Book(book_id).book_information()
            print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    print(f'下载耗时:{round(time.time() - start, 2)} 秒')


def shell():
    if len(sys.argv) > 1:
        command_line = True
        inputs = sys.argv[1:]
    else:
        command_line = False
        print(Vars.cfg.data.get('help'))
        inputs = re.split('\\s+', inputs_('>').strip())
    while True:
        if inputs[0].startswith('q') or inputs[0] == '--quit':
            sys.exit("已退出程序")
        if inputs[0] == 'h' or inputs[0] == '--help':
            print(Vars.cfg.data.get('help'))
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
    agreed_read_readme()

    shell()
