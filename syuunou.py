from pickletools import read_uint1
import re
from statistics import mean
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import os
from config import File


app = Flask(__name__)

@app.route("/add", methods=["POST"])
def addFamilyPost():
    name = request.form["syuunoumonomemo"]
    basyo = request.form["syuunoumonobasyo"]
    file = request.files["syuunounomono"]
    memo = request.form["syuunouziyuu"]
    kouho = request.form["syuunoukouho"]
    syurui = request.form["syuunousyurui"]
    hiniti = request.form["syuunouhiniti"]
    if basyo:
        basyo_name = basyo
    else:
        basyo_name = kouho
    file_name = str(file.filename)
    file_path = "static/images/" + file_name
    file.save(os.path.join('static/images/', file_name))
    File.create(name=name, file=file_path, basyo=basyo_name, memo=memo,syurui=syurui,hiniti=hiniti)
    return redirect("/syuunouapuri")


@app.route('/')
def syuunou():
    return render_template("hazime.html")

@app.route("/a")
def a():
    return render_template("a.html")

@app.route("/syuunouapuri")
def syuunouapuri():
    return render_template("syuunouapuri.html")

@app.route('/urlparam/<name>/<age>')
def urlparam(name,age):
    return render_template("urlparam.html",name=name,age=age)

@app.route("/syuunoutuika")
def syuunoutuika():
    return render_template("syuunoutuika.html")

@app.route("/syuunousyasinn")
def syuunousyasinn():
    search_text = request.args.get("search_text","")
    if not search_text:
        file = File.select()
    else:
        file = File.select().where(
            (File.name).contains(search_text)|
            (File.basyo).contains(search_text)|
            (File.syurui).contains(search_text)|
            (File.memo).contains(search_text))
    return render_template("syuunousyasinn.html",file=file,search_text=search_text)

@app.route("/delete/<id>")
def download(id):
    file = File.get(File.id == id)
    file_path = file.file
    os.remove(file_path)
    file.delete_instance()  
    return redirect("/syuunousyasinn")

@app.route("/detail/<id>")
def detail(id):
    file = File.get(File.id == id)
    return render_template("detail.html", file=file)

@app.route("/update/<id>", methods=["POST"])
def updateFamilyPost(id):
    name = request.form["syuunoumonomemo"]
    basyo = request.form["syuunoumonobasyo"]
    file = request.files["syuunounomono"]
    memo = request.form["syuunouziyuu"]
    kouho = request.form["syuunoukouho"]
    syurui = request.form["syuunousyurui"]
    hiniti = request.form["syuunouhiniti"]
    f = File.get(File.id == id)
    if file:
        file_name = str(file.filename)
        file_path = "static/images/" + file_name
        file.save(os.path.join('static/images/', file_name))
        f.file=file_path
    if basyo:
        basyo_name = basyo
    else:
        basyo_name = kouho
    f.name=name
    f.basyo=basyo_name
    f.memo=memo
    f.syurui=syurui
    f.hiniti=hiniti
    f.save()
    return redirect("/syuunousyasinn")

@app.route("/tukaikata")
def tukaikata():
    return render_template("tukaikata.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/touroku")
def touroku():
    return render_template("touroku.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)