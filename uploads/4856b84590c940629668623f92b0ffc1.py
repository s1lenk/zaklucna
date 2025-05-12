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

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

db = TinyDB('user.json')
user_table = db.table('user')
repository_db = TinyDB('repositories.json')
repository_table = repository_db.table('repository')
User = Query()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'py', 'html', 'css', 'js', 'txt', 'md', 'json', 'xml', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file selected'})
        
        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected!'})
        
        if file and allowed_file(file.filename):
            # Create a unique filename to store the file
            original_filename = file.filename
            file_extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
            unique_filename = f"{uuid.uuid().hex}.{file_extension}"

            #save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            #update repository in the database
            current_time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            new_file = {
                'original_filename': original_filename,
                'stored_filename': unique_filename,
                'date_uploaded': current_time,
                'file_size': os.path.getsize(file_path),
                'extension': file_extension
            }

            files = repository.get('files', [])
            files.append(new_file)

            repository_db.update({'files': files},
                                 (User.user == username) & (User.repository_name == repository_name))
            
            return jsonify({'success': True})
        else:
            allowed_extensions_list = ', '.join(ALLOWED_EXTENSIONS)
            return jsonify({'success': False, 'error': f'File type not allowed. Allowed types: {allowed_extensions_list}'})
        
    except Exception as e:
        print(f"An error occured while trying to add text to the repository: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to add text to the repository'})
    

@app.route('/view/<repository_name>/<stored_filename>')
def view_file(repository_name, stored_filename):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    repository = repository_db.get((User.user == username) & (User.repository_name == repository_name))

    if not repository:
        return redirect(url_for('mainPage'))
    
    # Find the file in the repository
    file_info = None
    for file in repository.get('files', []):
        if file['stored_filename'] == stored_filename:
            file_info = file
            break
    
    if not file_info:
        return redirect(url_for('view_repository', repopsitory_name=repository_name))
    
    # Read file content
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
        with open(file_path, 'r') as f:
            file_content = f.read()

        return render_template('view_file.html',
                               repository=repository,
                               file_info=file_info,
                               file_content=file_content)
    
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return redirect(url_for('view_repository', repository_name=repository_name))



if __name__ == "__main__":
    # Ustvari direktorij za predloge, če ne obstaja
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)
    