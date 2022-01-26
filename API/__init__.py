from API.Settings import *
from API import HttpUtil, UrlConstants


class Book:

    @staticmethod
    def novel_info(novel_id: int):
        return HttpUtil.get(UrlConstants.BOOK_INFO_API.format(novel_id))

    @staticmethod
    def catalogue(novel_id: int):
        return HttpUtil.get(UrlConstants.BOOK_CATALOGUE.format(novel_id))

    @staticmethod
    def search_book(novel_name: str):
        return HttpUtil.get(UrlConstants.SEARCH_API.format(novel_name))


class Chapter:
    @staticmethod
    def download_chapter(chapter_id: str):
        return HttpUtil.get(UrlConstants.CHAPTER_API.format(chapter_id))


class Cover:
    @staticmethod
    def get_cover():
        return HttpUtil.get('http://119.91.108.170:88/api/img/acg.php?return=json')

    @staticmethod
    def download_cover(cover_josn: dict):
        return HttpUtil.cover(cover_josn.get('acgurl'))


class Tag:
    @staticmethod
    def get_type():
        return HttpUtil.get(UrlConstants.GET_TYPE_INFO).get('male')

    @staticmethod
    def tag_info(tag_id, tag_name, page):
        return HttpUtil.get(UrlConstants.TAG_API.format(tag_id, tag_name, page))

    @staticmethod
    def ranking(ranking_num):
        return HttpUtil.get(UrlConstants.RANKING_API.format(ranking_num))
