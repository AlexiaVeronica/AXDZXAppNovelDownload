import book
from function.instance import *
from API import HttpUtil, UrlConstants


class SearchBook:
    def __init__(self, book_name):
        self.search_api = UrlConstants.SEARCH_API.format(book_name)
        self.response = HttpUtil.get(self.search_api)

    def search_book(self):
        for books in self.response.get('books'):
            if Vars.cfg.data.get('Epub'):
                book_id = books.get('_id')
                book.Book(book_id).book_information()
            else:
                book.Book(books.get('_id')).book_information()
