from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
import os
import requests
import uuid

app = Flask(__name__)
app.secret_key = "holou_nit_skong_jvelin"

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = TinyDB('user.json')
user_table = db.table('user')
repository_db = TinyDB('repositories.json')
repository_table = repository_db.table('repository')
User = Query()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'py', 'html', 'css', 'js', 'txt', 'md', 'json', 'xml', 'csv'}

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
    bad_characters = """!#$%&()*+,-./:;<=>?@[]"^`{|}~'"""

    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try: 
        repository_name = request.form['repository_name']
        username = session['username']

        for bc in bad_characters:
            if bc in repository_name:
                return jsonify({'success': False, 'error': 'The name of the repository cannot include special characters'})

        existing_repository = repository_db.get((User.user == username) & (User.repository_name == repository_name))

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
    

@app.route("/view_repository/<repository_name>")
def view_repository(repository_name):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    username = session['username']
    repository = repository_db.get((User.user == username) & (User.repository_name == repository_name))

    if not repository:
        return redirect(url_for("mainPage"))

    return render_template("repository.html", repository=repository)


@app.route('/delete_repository', methods=['POST'])
def delete_repository():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try:
        username = session['username']
        repository_name = request.form['repository_name']

        repository = repository_db.get((User.user == username) & (User.repository_name == repository_name))

        if not repository:
            return jsonify({'success': False, 'error': 'Could not delete repository'})
        
        repository_db.remove((User.user == username) & (User.repository_name == repository_name))

        return jsonify({'success': True})

    except Exception as e:
        print(f"An error occured while trying to delete the repository: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to delete the repository'})


@app.route('/add_file', methods=['POST'])
def add_file():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try: 
        repository_name = request.form['repository_name']
        username = session['username']

        repository = repository_db.get((User.user == username) & (User.repository_name == repository_name))

        if not repository:
            return jsonify ({'success': False, 'error': 'Repository not found'})
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file selected'})

    except Exception as e:
        print(f"An error occured while trying to add text to the repository: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to add text to the repository'})


if __name__ == "__main__":
    # Ustvari direktorij za predloge, če ne obstaja
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)
    