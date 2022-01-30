import API
import book
from API.Settings import *
from function import tag, ranking


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
        start = time.time()
        book.Book(inputs[1]).book_information()
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
    else:
        print('未输入Bookid')


def shell_search_book(inputs):
    """搜索书名下载小说"""
    if len(inputs) >= 2:
        start = time.time()
        for books in API.Book.search_book(inputs[1]).get('books'):
            book_id = books.get('_id')
            book.Book(book_id).book_information()
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
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
    if len(inputs) >= 2:
        tag_id = inputs[1]
        if not Vars.cfg.data.get('tag').get(tag_id):
            print(f"{tag_id} 标签号不存在\n", Vars.cfg.data.get('tag'))
        else:
            tag.Tag(tag_id).tag_information()
    else:
        print(Vars.cfg.data.get('tag'))


def shell_ranking(inputs):
    if len(inputs) >= 2:
        ranking_num = inputs[1]
        ranking.ranking_(ranking_num)
    else:
        ranking_dict = {'周榜': '1', '月榜': '2', '总榜': '3'}
        for key, Value in ranking_dict.items():
            print('{}:\t\t\t{}'.format(key, Value))


def shell_list(inputs):
    start = time.time()
    if len(inputs) >= 2:
        list_file_name = inputs[1] + '.txt'
    else:
        list_file_name = 'list.txt'
    try:
        list_file_input = open(list_file_name, 'r', encoding='utf-8')
    except OSError:
        print(f"{list_file_name}文件不存在")
        return
    list_lines = list_file_input.readlines()
    for line in list_lines:
        if re.match("^\\s*([0-9]{1,7}).*$", line):
            start = time.time()
            book_id = re.sub("^\\s*([0-9]{1,7}).*$\\n?", "\\1", line)
            book.Book(book_id).book_information()
            end = time.time()
            print(f'下载耗时:{round(end - start, 2)} 秒')
    end = time.time()
    print(f'下载耗时:{round(end - start, 2)} 秒')


def shell():
    print(Vars.cfg.data.get('help'))
    agreed_read_readme()
    if len(sys.argv) > 1:
        inputs = sys.argv[1:]

    else:
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
        elif inputs[0] == 'u' or inputs[0] == '--updata':
            shell_list(inputs)
        elif inputs[0] == 'p' or inputs[0] == '--pool':
            get_pool(inputs)
        else:
            print(inputs[0], '不是有效命令')
        inputs = re.split('\\s+', inputs_('>').strip())


if __name__ == '__main__':
    shell()
