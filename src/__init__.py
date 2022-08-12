from src import HttpUtil, UrlConstants


class Book:

    @staticmethod
    def novel_info(novel_id: int):
        return HttpUtil.get(UrlConstants.BOOK_INFO_API.format(novel_id)).json

    @staticmethod
    def catalogue_info(novel_id: int) -> dict:
        return HttpUtil.get(UrlConstants.BOOK_CATALOGUE.format(novel_id)).retry()

    @staticmethod
    def search_book(novel_name: str):
        return HttpUtil.get(UrlConstants.SEARCH_API.format(novel_name)).json.get('books')


class Chapter:
    @staticmethod
    def download_chapter(chapter_id: str):
        return HttpUtil.get(UrlConstants.CHAPTER_API.format(chapter_id)).json


class Cover:
    @staticmethod
    def download_cover(max_retry=10) -> bytes:
        for retry in range(max_retry):
            params = {'type': 'moe', 'size': '1920x1080'}
            response = HttpUtil.get('https://api.yimian.xyz/img', params=params, app=False)
            if response.code == 200:
                return HttpUtil.get(response.request_url).content
            else:
                print("msg:", response.string)


class Tag:
    @staticmethod
    def get_type():
        type_dict = {}
        response = HttpUtil.get(UrlConstants.GET_TYPE_INFO).json
        for number, sort in enumerate(response['male']):
            number += 1
            major = sort.get('major')
            type_dict[number] = major
        return type_dict

    @staticmethod
    def tag_info(tag_id, tag_name, page):
        book_list = HttpUtil.get(UrlConstants.TAG_API.format(tag_id, tag_name, page)).json
        if book_list['books']:
            return book_list['books']

    @staticmethod
    def ranking(ranking_num):
        return HttpUtil.get(UrlConstants.RANKING_API.format(ranking_num)).json
