from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
import os
import requests

app = Flask(__name__)
app.secret_key = "holou_nit_skong_jvelin"

db = TinyDB('user.json')
user_table = db.table('user')
repository = db.table('repository')
User = Query()


@app.route("/")
def mainPage():
    if 'username' in session:
        return render_template("mainPage.html")
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            user_record = user_table.get(User.username == username)

            if user_record:
                if user_record['password'] == password:
                    session['username'] = username

                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False, 'error': 'Napačno geslo'})
            else:
                user_table.insert({'username': username, 'password': password})
                session['username'] = username
                return jsonify({'success': True})
        
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == "__main__":
    # Ustvari direktorij za predloge, če ne obstaja
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)