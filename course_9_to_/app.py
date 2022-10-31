from flask import Flask #載入flask
from flask import request #載入flask的request, 用來接收/觀察前端丟過來的請求
from flask import render_template #載入render_template使用樣板引擎

#建Flask 的application物件, 可以設定靜態檔案的路徑處理
app = Flask(__name__,
            static_folder = 'public', #放置靜態檔案的資料夾名稱
            static_url_path = '/' #靜態檔案對應的網址路徑 (只給/就是網址裡面路徑/後面直接接上public資料夾內的檔案名稱就會吃到靜態檔案)
) 

#使用 GET 方法 處理路徑 / 的對應函式
@app.route("/")
def index():
    return render_template('index.html')

#使用 GET 方法 處理路徑 /page 的對應函式
@app.route("/page")
def index_page():
    return render_template('page.html')

#使用 GET 方法 處理路徑 /show 的對應函式
@app.route("/show")
def show():
    name = request.args.get("n", "")
    return "Welcom " + name + ", thsi is in show page"

#使用 POST 方法 處理路徑 /calculate 的對應函式
@app.route("/calculate", methods=["POST"])
def calculate():
    #GET方法取得Query string
    # maxNumber = request.args.get("max", "")
    #POST方法取得Query string
    maxNumber = request.form["max"]
    maxNumber = int(maxNumber)
    result=0
    for i in range(1, maxNumber+1):
        result = result + i
    return render_template('result.html',
                            calculate_result =result ) #把後端計算的結果塞到html



#啟動伺服器, 可透過參數port修改port的設定,預設是5000
app.run(port=3000) 