from flask import Flask #載入flask
from flask import request #載入flask的request, 用來接收/觀察前端丟過來的請求
from flask import redirect #載入 redirect, 用來做重新導向
from flask import render_template #載入render_template使用樣板引擎
import json
#建Flask 的application物件, 可以設定靜態檔案的路徑處理
app = Flask(__name__,
            static_folder = 'pulic', #放置靜態檔案的資料夾名稱
            static_url_path = '/mystatic' #靜態檔案對應的網址路徑
) 
# 所有在pulic資料夾底下的檔案ㄝ都對應的網址路徑 /mystatic/檔案名稱


#建立路徑 /en 對應的處裡函式
@app.route('/en')
def index_english(): #用來回應路徑 /en的函式
    return render_template('index_en', #render_template預設所有樣板都一定要放在 templates 資料夾底下
                            name = 'WCLEEZA',
                            json_content = json.dumps({
                                            "status": "ok",
                                            "text" : "welcome to Flask"
                                        })) #樣板引琴好用的地方在於可以自訂變數連動到樣板內容 (需要遵守變數定義語法{{xxxx}})

#建立路徑 /zh 對應的處裡函式
@app.route('/zh')
def index_chinese(): #用來回應路徑 /zh的函式
    return json.dumps({
        "status": "ok",
        "text" : "您好, 歡迎來到Flask"
    }, ensure_ascii=False )#回傳首頁的內容 (ensure_ascii=False 是要求json不用只用ascii去解碼)

#建立路徑 / 對應的處裡函式
@app.route('/')
def index(): #用來回應路徑 /的函式
    # return redirect('/en') #如果只給片段, flask就會把這個片段加在url的路徑部分
    # return redirect('https://google.com/') #如果給完整網址, 就會導向這個網址

    #這邊是看前端訪問我們時,呼叫的url以及使用的http的協定,方法
    print(f'請求方法 : {request.method}')
    print(f'通訊協定 : {request.scheme}')
    print(f'主機名稱 : {request.host}')
    print(f'路徑 : {request.path}')
    print(f'完整的網址 : {request.url}')

    #這邊是看前端訪問我們的時候,提供的額外資訊(這些資訊都存在headers裡面)
    print(f'前端的瀏覽器和作業系統 {request.headers.get("user-agent")}')
    print(f'前端的語言偏好 {request.headers.get("accept-language")}')
    print(f'引薦網址 {request.headers.get("referrer")}')

    #依照使用者瀏覽器的語言偏好,切換不同的顯示
    lang = request.headers.get("accept-language")
    if lang.startswith('en'):
        return redirect("/en")
        
    else:
        return redirect("/zh")
        
#建立路徑 /data 對應的處裡函式
@app.route('/data')
def handleData(): #用來回應路徑 /data 的函式

    return 'My data' #回傳首頁的內容

#建立動態路徑 /user/使用者名稱 對應的處裡函式
@app.route('/user/<username>')
def handleUser(username): #用來回應動態路徑 /user/使用者名稱 的函式
    if username == '緯節':
        return '你好 ' + username  #回傳首頁的內容
    else:
        return 'Hello ' + username  #回傳首頁的內容


#建立路徑 /getSum 對應的處裡函式
#利用要求字串(query string)提供彈性 : /getSum?min=加總起點&max=加總終點
@app.route("/getSum")
def getSum():
    #取得要求字串裡面的資料
    query_string_min = request.args.get('min', None)
    query_string_max = request.args.get('max', None)
    print(f'網址裡面的要求字串"min" and "max"為 : {query_string_min}/{query_string_max}')
    #利用要求字串的資料作處理
    if  query_string_min and query_string_max:
        result = 0
        for i in range(int(query_string_min), int(query_string_max)+1):
            result = result + i
        return_string = f'Sum result from {query_string_min} to {query_string_max} =  {result}'
        return return_string
    else:
        return "No Query String ('min' or 'max') provided!!"







#啟動伺服器, 可透過參數port修改port的設定,預設是5000
app.run(port=3000) 


    
