import book
from function.instance import *
import API


def ranking_(ranking_num):
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
    for novel_id in novel_list:
        book.Book(novel_id).book_information()
