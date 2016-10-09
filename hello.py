from imdb_parser import *
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def hello():
    l = get_all()
    return render_template("index.html",l=l)


@app.route("/add",methods = ["POST","GET"])
def add():
    if request.method == 'POST':
        title = request.form['title']
        print title
        rows = add_tv(title)
        return redirect(url_for('hello'))
if __name__ == "__main__":
            app.run(debug=True)


