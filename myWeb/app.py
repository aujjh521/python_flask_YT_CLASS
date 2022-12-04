#初始化mongodb server連線
import pymongo
import certifi #在連線到mongodb cluster的時候需要用到
client = pymongo.MongoClient("mongodb+srv://aujjh521:1003@mycluster.iyd1nxs.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where()) #記得替換掉自己的密碼
db = client.member_system #選擇操作 member_system 資料庫 (client物可以創建一個database, 這邊取名叫 member_system, 如果已經存在則使用該database)
print(f'mongodb資料庫連線成功!')


#初始化flask伺服器
from flask import *

#為了inference
import urllib.request
from kernels.DogCatClassification.inference import *

#建Flask 的application物件, 可以設定靜態檔案的路徑處理
app = Flask(__name__,
            static_folder = 'public', #放置靜態檔案的資料夾名稱
            static_url_path = '/' #靜態檔案對應的網址路徑 (只給/就是網址裡面路徑/後面直接接上public資料夾內的檔案名稱就會吃到靜態檔案)
) 

#要使用session之前需要先定義secret_key (因為session會做加密)
app.secret_key = "any string but keep secret" 

#處裡首頁的路由
@app.route("/")
def index():
    return render_template("index.html")

#處裡會員頁面的路由
@app.route("/member")
def member():
    #利用session做權限控管,只有經過登入在session裡面存入nickname的人才可以進入member頁面
    if "nickname" in session:
        return render_template("member.html",
                                member_nickname = session["nickname"])
    else:
        #沒有經過登入在session裡面存入nickname的人就不是會員,導回首頁
        return redirect("/")

#錯誤頁面的路由 (搭配要求字串)
@app.route("/error")
def error():
    message = request.args.get("msg", "發生錯誤 請聯絡客服")
    return render_template("error.html",
                            err_msg =  message)

#圖片下載失敗頁面的路由 (搭配要求字串)
@app.route("/GetImgFail")
def GetImgFail():
    message = request.args.get("msg", "發生錯誤 請聯絡客服")
    return render_template("getimagefail.html",
                            err_msg =  message)

@app.route("/signup", methods=["POST"])
def signup():
    #從前端取得資料
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    #print(nickname, email, password)

    #根據資料跟資料庫作互動
    collection = db.user
    #檢查資料庫中是否已經存在這組email
    doc = collection.find_one({
        "email":email
    })
    if doc != None:
        return redirect("/error?msg=此信箱已經被註冊過了")
    else:
        collection.insert_one({
            "email":email,
            "nickname":nickname,
            "password":password
        })
        return redirect("/") #註冊成功之後回到首頁

@app.route("/signin", methods=["POST"])
def signin():
    #從前端取得資料
    email = request.form["email"]
    password = request.form["password"]
    #print(nickname, email, password)

    #根據資料跟資料庫作互動
    collection = db.user
    #檢查資料庫中是否已經存在這組email/密碼
    doc = collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })

    #有抓到doc代表登入成功, 先在session裡面存入nickname之後導向member頁面
    if doc != None:
        session["nickname"] = doc["nickname"]
        return redirect("/member") 
    #登入失敗
    else:
        return redirect("/error?msg=帳號/密碼錯誤") #帳密錯誤


#處裡貓狗分類的路由
@app.route("/DogCatClassification")
def DogCatClassification():
    #利用session做權限控管,只有經過登入在session裡面存入nickname的人才可以進入member頁面
    if "nickname" in session:
        return render_template("DogCatClassification.html",
                                member_nickname = session["nickname"])
    else:
        #沒有經過登入在session裡面存入nickname的人就不是會員,導回首頁
        return redirect("/")

#處裡貓狗分類執行預測的路由
@app.route("/DogCatClassification_predict",  methods=["POST"])
def DogCatClassification_predict():
    #利用session做權限控管,只有經過登入在session裡面存入nickname的人才可以進入member頁面
    if "nickname" in session:

        #save image to local folder
        try:
            img_url = request.form["imgurl"]
            print('get img from url success')
            local_path = "./public/download/" + "local-filename.jpg"
            urllib.request.urlretrieve(img_url, local_path)
            print(f'save image to local folder')
        except Exception as e:
            print(e)
            return redirect("/GetImgFail?msg=該圖片無法被下載,請更換其他圖片網址")

        #load ML model
        model = CNN()
        model.load_state_dict(torch.load(pretrained_weight_path,map_location=torch.device("cpu")))

        #%%
        #inference
        test_transform = transforms.Compose([transforms.Resize((128, 128)),
                            transforms.ToTensor()
                            ])

        img = Image.open(local_path)
        img = test_transform(img).unsqueeze(0) #增加一個維度for batch
        res = model(img)

        #把predict結果mapping回初始類別
        _, pred = torch.max(res, dim=1)
        label_encode_mapping = {1:'dog',
                    0:'cat'
                    }
        
        return render_template('DogCatClassification_result.html',
                                member_nickname = session["nickname"],
                                predicted_label = label_encode_mapping[pred.numpy()[0]],
                                target_image = "/download/"+"local-filename.jpg")

    else:
        #沒有經過登入在session裡面存入nickname的人就不是會員,導回首頁
        return redirect("/")


@app.route("/signout")
def signout():
    #移除session中的會員資訊
    del session["nickname"]
    return redirect("/")

#啟動伺服器, 可透過參數port修改port的設定,預設是5000
app.run(port=3000) 