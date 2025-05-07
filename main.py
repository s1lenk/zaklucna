from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
import os
import requests

app = Flask(__name__)
app.secret_key = "holou_nit_skong_jvelin"

db = TinyDB('user.json')
user_table = db.table('user')
repository_db = TinyDB('repositories.json')
User = Query()

@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/mainPage", methods=['POST', 'GET'])
def mainPage():
    if 'username' in session:
        username = session['username']
        repositories = repository_db.search(User.user == username)
        return render_template("mainPage.html", repositories = repositories)
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
            print(f"An error occured while logging in: {str(e)}")
            return jsonify({'success': False, 'error': 'An error occured while logging in'})
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/account_settings')
def account_settings():
    return 


@app.route('/create_repository', methods=['POST'])
def create_repository():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try: 
        repository_name = request.form['repository_name']
        username = session['username']

        existing_repository = repository_db.get((User.username == username) & (User.repository_name == repository_name))

        if existing_repository:
            return jsonify({'success': False, 'error': 'Repository already exists'})
        
        repository_db.insert({
            'user': username,
            'repository_name': repository_name,
            'date of creation': datetime.now().strftime("%H:%M:%S %d-%m-%Y"),
            'files': []
        })

        

        return jsonify({'success': True})

    except Exception as e:
        print(f"An error occured while trying to create a repository: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to create a repository'})
    

@app.route('/add_file', methods=['POST'])
def add_text_to_repos():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try: 
        repository_name = request.form['repository_name']
        username = session['username']


    except Exception as e:
        print(f"An error occured while trying to add text to the repository: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to add text to the repository'})



if __name__ == "__main__":
    # Ustvari direktorij za predloge, če ne obstaja
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)
    