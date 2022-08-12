from src import HttpUtil, UrlConstants, epub


class Book:

    @staticmethod
    def novel_info(novel_id: int) -> dict:
        return HttpUtil.get(UrlConstants.BOOK_INFO_API.format(novel_id)).retry()

    @staticmethod
    def catalogue_info(novel_id: int) -> dict:
        return HttpUtil.get(UrlConstants.BOOK_CATALOGUE.format(novel_id)).retry()

    @staticmethod
    def search_book(novel_name: str) -> dict:
        return HttpUtil.get(UrlConstants.SEARCH_API.format(novel_name)).retry()

    @staticmethod
    def download_chapter(chapter_id: str) -> dict:
        return HttpUtil.get(UrlConstants.CHAPTER_API.format(chapter_id)).retry()


class Cover:
    @staticmethod
    def download_cover() -> bytes:
        params = {'type': 'moe', 'size': '1920x1080'}
        response = HttpUtil.get('https://api.yimian.xyz/img', params=params, app=False).retry(return_type="")
        return HttpUtil.get(response.url).content


class Tag:
    @staticmethod
    def get_tag_type_information():
        type_dict = {}
        response = HttpUtil.get(UrlConstants.GET_TYPE_INFO).retry()
        for number, sort in enumerate(response['male']):
            number += 1
            major = sort.get('major')
            type_dict[number] = major
        return type_dict

    @staticmethod
    def tag_info(tag_id, tag_name, page) -> dict:
        return HttpUtil.get(UrlConstants.TAG_API.format(tag_id, tag_name, page)).retry()

    @staticmethod
    def ranking(ranking_num) -> dict:
        return HttpUtil.get(UrlConstants.RANKING_API.format(ranking_num)).json
