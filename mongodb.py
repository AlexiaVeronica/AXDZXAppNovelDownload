import pymongo


class MongoDb:
    def __init__(self, db_name, collection_name, host="mongodb://localhost:27017/"):
        self.client = pymongo.MongoClient(host)  # host uri
        self.get_mongodb = self.client[db_name]
        self.collection = self.get_mongodb[collection_name]

    def insert_data(self, data):
        self.collection.insert_one(data)

    def find_data(self) -> list:
        return [i for i in self.collection.find()]

    def find_data_by_id(self, book_id: str):
        return self.collection.find_one({"_id": str(book_id)})

    def find_data_by_book_id(self, book_id: str):
        return self.collection.find_one({"book_id": str(book_id)})

    def find_data_by_novel_finish(self, novel_finish):
        return [i for i in self.collection.find({"novel_finish": novel_finish})]

    def find_data_by_chapter_id(self, chapter_id):
        return [i for i in self.collection.find({"chapter_id": chapter_id})]

    def find_data_by_chapter_title(self, chapter_title):
        return [i for i in self.collection.find({"title": chapter_title})]

    def find_data_by_keyword(self, keyword):
        search_list = []
        for data in self.collection.find():
            if keyword in data["novel_name"] or keyword in data["novel_intro"] or \
                    keyword in data["novel_author"]:
                search_list.append(data)
        return search_list


# 图片转base64
def img_to_base64(img_path):
    import base64
    with open(img_path, "rb") as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
    return s
