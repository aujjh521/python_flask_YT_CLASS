#初始化flask伺服器
from flask import *

#建Flask 的application物件, 可以設定靜態檔案的路徑處理
app = Flask(__name__) 


#處裡首頁的路由
@app.route("/")
def index():
    return "Hellow World"

#啟動伺服器, 可透過參數port修改port的設定,預設是5000
app.run(port=3000) 