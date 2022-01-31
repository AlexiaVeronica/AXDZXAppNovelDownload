from API.Settings import *
from API import HttpUtil, UrlConstants
import ahttp


def get(api_url: str):
    api_url = UrlConstants.WEB_SITE + api_url.replace(UrlConstants.WEB_SITE, '')
    return HttpUtil.get(api_url)


class Book:

    @staticmethod
    def novel_info(novel_id: int):
        return get(UrlConstants.BOOK_INFO_API.format(novel_id))

    @staticmethod
    def catalogue(novel_id: int):
        return get(UrlConstants.BOOK_CATALOGUE.format(novel_id))

    @staticmethod
    def search_book(novel_name: str):
        return get(UrlConstants.SEARCH_API.format(novel_name))


class Chapter:
    @staticmethod
    def download_chapter(chapter_id: str):
        return get(UrlConstants.CHAPTER_API.format(chapter_id))


class Cover:
    @staticmethod
    def get_cover():
        api_url = 'http://119.91.108.170:88/api/img/acg.php?return=json'
        return HttpUtil.cover(api_url).json()

    @staticmethod
    def download_cover(cover_josn: dict):
        return HttpUtil.cover(cover_josn.get('acgurl')).content


class Tag:
    @staticmethod
    def get_type():
        return get(UrlConstants.GET_TYPE_INFO).get('male')

    @staticmethod
    def tag_info(tag_id, tag_name, page):
        api_url = UrlConstants.WEB_SITE + UrlConstants.TAG_API.format(tag_id, tag_name, page)
        return ahttp.get(api_url)

    @staticmethod
    def ranking(ranking_num):
        return get(UrlConstants.RANKING_API.format(ranking_num))
