from flask import Flask
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session
import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError
#加密
from werkzeug.security import generate_password_hash, check_password_hash


#初始化資料庫連線
try:
    client = pymongo.MongoClient("mongodb+srv://ryley0401:admin@oneselect.mrsaxx1.mongodb.net/")
    client.admin.command('ping')
    db = client.member_system
    print("資料庫連線成功")
except ConnectionFailure:
    print('無法連線到資料庫')
except PyMongoError as e:
    print(f"其他pymongo錯誤：{ e }")





app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "oneselectkey"

@app.route('/')
def root():
    return redirect(url_for('oneselect'))

#首頁路由
@app.route("/oneselect")
def oneselect():
    return render_template("index.html")

#註冊頁面設定
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")
        birthday = request.form.get("birthday", "")
        gender = request.form.get("gender", "")
        #基本欄位檢查
        if not username or not password or not confirm_password or not email:
            flash("請填寫所有必填欄位")
            return render_template("signup.html")
        if password != confirm_password:
            flash("兩次輸入的密碼不一致")
            return render_template("signup.html")
        collection = db.users
        if collection.find_one({"username" : username}):
            flash("此帳號已被註冊，請重新輸入")
            return render_template("signup.html")
        if collection.find_one({"email" : email}):
            flash("信箱已被使用，請更換一個信箱")
            return render_template("signup.html")
        #密碼加密
        hashed_password = generate_password_hash(password)

        #寫入資料庫
        user_data = {
            'username' : username,
            'password' : hashed_password,
            'email' : email,
            'birthday' : birthday,
            'gender' : gender
        }
        collection.insert_one(user_data)
        flash("註冊成功，請登入")
        return redirect(url_for("login"))
    return render_template("signup.html")

#登入頁面設定
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #從前端取得使用者輸入的帳號，密碼
        username = request.form.get("username")
        password = request.form.get("password")
        collection = db.users
        user = collection.find_one({
            "username" : username
        })
        if not user:
            flash("帳號輸入錯誤，請重新輸入")
            return render_template("login.html")
        if not check_password_hash(user["password"], password):
            flash("密碼輸入錯誤，請重新輸入")
            return render_template("login.html")
        
        #登入若成功，儲存session
        session["username"] = username
        flash("登入成功")
        #跳轉回首頁
        return redirect(url_for("oneselect"))
    #如果method不是POST，就導回登入頁面
    return render_template("login.html")

#登出會員
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("已成功登出")
    return redirect(url_for("login"))





#服飾頁面路由
@app.route("/cloth")
def cloth():
    return render_template("cloth.html")

#雜貨首頁
@app.route("/Groceries")
def Groceries():
    return render_template("Groceries.html")

#鞋類首頁
@app.route("/shoes")
def shoes():
    return render_template("shoes.html")

#所有商品頁面
@app.route("/all")
def all():
    return render_template("all.html")




if __name__ == '__main__':
    app.run(debug=True)
