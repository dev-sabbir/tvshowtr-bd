from imdb_parser import *
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
msg =""
@app.route("/")
def hello():
    l = get_all()
    global msg
    return render_template("index.html",l=l,msg=msg)


@app.route("/add",methods = ["POST","GET"])
def add():
    global msg
    msg=""
    if request.method == 'POST' and request.form['title']!="":
        title = request.form['title']
        print title
        rows = add_tv(title)
        return redirect(url_for('hello'))
    else:
        msg = "Don't insert wrong input. Try something like this: tt3107288"
        return redirect(url_for('hello'))
if __name__ == "__main__":
            app.run(debug=True)


