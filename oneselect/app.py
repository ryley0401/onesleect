from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route('/')
def root():
    return redirect(url_for('oneselect'))

#首頁路由
@app.route("/oneselect")
def oneselect():
    return render_template("index.html")

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
