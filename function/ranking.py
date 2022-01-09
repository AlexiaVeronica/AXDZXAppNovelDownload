import book
from function.instance import *
from API import UrlConstants, HttpUtil

class Rank:
    def __init__(self, ranking_num):
        self.bookid_list = []
        self.ranking_api = 'http://api.aixdzs.com/ranking/{}'
        self.rank_result = HttpUtil.get(self.ranking_api.format(ranking_num))
        self.books_result = self.rank_result.get('ranking').get('books')
        # print(self.rank_result)
        
    def rank_(self):
        for data in self.books_result:
            for key, Value in data.items():
                if key == 'title':
                    print('\n\n{}:\t\t\t{}'.format(key, Value))
                    continue
                book_info = '{}:\t\t\t{}'.format(key, Value) if len(
                    key) <= 6 else '{}:\t\t{}'.format(key, Value)
                print(book_info)
            bookid = data.get('_id')
            self.bookid_list.append(bookid)
        for BOOKID in self.bookid_list:
            Download = book.Book(BOOKID)
            Download.book_information()
            