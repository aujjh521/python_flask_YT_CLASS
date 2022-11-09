# 載入mongodb package
import pymongo
import certifi #在連線到mongodb cluster的時候需要用到

# 連線到mongodb雲端資料庫
# 從官方取得的連線到cluster網址, 完成就可以拿到MongoClient物件, 存成變數client (注意這邊是連到cluster, cluster的裡面才可以創建database, 然後資料是存在database裡面的集合)
# Cluster --> Database --> Collection(存放資料)
client = pymongo.MongoClient("mongodb+srv://aujjh521:1003@mycluster.iyd1nxs.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where()) #記得替換掉自己的密碼

# 把資料放進資料庫中
db = client.mywebsite #選擇操作 mywebsite 資料庫 (client物可以創建一個database, 這邊取名叫 mywebsite, 如果已經存在則使用該database)
collection = db.users #選擇操作 users 集合 (在database裡面創建一個集合, 這邊取名叫 users, 如果已經存在則使用該集合)

# 把資料新增到集合中
# result = collection.insert_one({
#     "name": "丁滿",
#     "email": "tin@tin.com",
#     "password": "tin",
#     "level":2
# }) #mongodb裡面存的資料是json格式, json在python就是dict的概念

# print('資料新增成功!')
# print(f'該筆資料的id是{result.inserted_id}')



# 把多筆資料新增到集合中
# result = collection.insert_many([{
#     "name": "彭",
#     "email": "pp@pp.com",
#     "password": "pp",
#     "level":2
# }, {
#     "name": "嘎",
#     "email": "gg@gg.com",
#     "password": "gg",
#     "level":3

# }]) #mongodb裡面存的資料是json格式, json在python就是dict的概念

# print('一次新增多筆資料成功!')
# print(f'所有資料的id依序是{result.inserted_ids}')


# 取得集合中的第一筆資料
# data = collection.find_one()
# print(data)

# 根據ObjectId取得資料
# from bson.objectid import ObjectId
# data = collection.find_one(
#     ObjectId('636a4b334f981cef195fca7f')
# )
# print(data)


#取得集合中的所有文件
cursor = collection.find()
for doc in cursor:
    print(doc)
