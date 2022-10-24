
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mycol = mydb["links"]

mydict = {"id": 1, "date": 123, "link": "John", "path": "Highway 37"}

# x = mycol.insert_one(mydict)

for y in mycol.find().limit(1).sort([('$natural', -1)]):
    print(y['id'])
print(123)
for x in mycol.find():
    print(x)
