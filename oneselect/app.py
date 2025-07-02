from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__, static_folder="static", static_url_path="/static")

#首頁路由
@app.route("/oneselect")
def oneselect():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
