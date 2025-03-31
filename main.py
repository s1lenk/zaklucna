from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("mainPage.html")

@app.route("/login")
def login():
    return render_template("login.html")

app.run(debug=True)