
import pymongo


class MongoClient:
    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.__db = self.__client["mydatabase"]
        self.__collection = self.__db['links']

    def insert(self, file_id: int, link: str, path: str) -> None:
        self.__collection.insert_one({
            "file_id": file_id,
            "link": link,
            "path": path,
        })

    def find_last_doc_id(self) -> int:
        for doc in self.__collection.find().limit(1).sort([('$natural', -1)]):
            print(doc)
            if doc is None:
                return -1
            else:
                return doc

    def find_path(self, link) -> str:
        return self.__collection.find_one({"link": link})['path']

    def drop(self) -> None:
        self.__collection.delete_many({})

