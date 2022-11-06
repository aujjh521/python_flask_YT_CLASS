# 載入mongodb package
import pymongo
import certifi #在連線到mongodb cluster的時候需要用到

# 連線到mongodb雲端資料庫
# 從官方取得的連線到cluster網址, 完成就可以拿到MongoClient物件, 存成變數client (注意這邊是連到cluster, cluster的裡面才可以創建database, 然後資料是存在database裡面的集合)
# Cluster --> Database --> Collection(存放資料)
client = pymongo.MongoClient("mongodb+srv://aujjh521:1003@mycluster.iyd1nxs.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where()) #記得替換掉自己的密碼

# 把資料放進資料庫中
db = client.test #選擇操作 test 資料庫 (client物可以創建一個database, 這邊取名叫 test, 如果已經存在則使用該database)
collection = db.users #選擇操作 users 集合 (在database裡面創建一個集合, 這邊取名叫 users, 如果已經存在則使用該集合)
# 把資料新增到集合中
collection.insert_one({
    "name": "wcleeza",
    "gender": "男"
}) #mongodb裡面存的資料是json格式, json在python就是dict的概念

print('資料新增成功!')
