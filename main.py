from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = "holou_nit_skong_jvelin"

db = TinyDB('user.json')
user =  db.table('user')
repository = db.table('repository')
User = Query()


@app.route("/")
def mainPage():
    return render_template("mainPage.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

app.run(debug=True)