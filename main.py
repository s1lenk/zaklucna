from flask import Flask, render_template, redirect, url_for, session, request, jsonify, send_file
from tinydb import TinyDB, Query
from datetime import datetime
import os
import uuid
import re

app = Flask(__name__)
app.secret_key = "holou_nit_skong_jvelin"

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

db = TinyDB('static/json/user.json')
user_table = db.table('user')
repository_db = TinyDB('static/json/repositories.json')
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
                user_table.insert({
                    'username': username, 
                    'password': password,
                    'friends': []
                })
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
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    return render_template('account_settings.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    if request.method == 'POST':
        try:
            username = session['username']
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_new_password = request.form['confirm_new_password']

            current_user_data = user_table.get((User.password == old_password) and (User.username == username))

            if not current_user_data:
                return jsonify({'success': False, 'error': 'Old password does not match!'})
            
            if new_password != confirm_new_password:
                return jsonify({'success': False, 'error': 'New password does not match confirme password!'})

            user_table.update({'password': new_password},
                            (User.username == username)) 
            
            return jsonify({'success': True, 'message': 'You password has been changed'})
        
        except Exception as e:
            print(f"An error occured while trying to change password {str(e)}")
            return jsonify({'success': False, 'error': 'An error occured while trying to change password!'})
    else:
        return render_template('change_password.html')


@app.route('/community_page', methods=['GET'])
def community_page():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    return render_template('community_page.html', )

@app.route('/search_for_user', methods=['POST'])
def search_for_user():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try:
        searched_username = request.form['searched_username']
        # current_username = session['username']

        searched_username_pattern = f".*{searched_username}.*"
        search_username_result = user_table.search(User.username.matches(searched_username_pattern, flags=re.IGNORECASE))
        
        if search_username_result:
            user_data = []

            for user in search_username_result:
                user_data.append({
                    'username': user['username']
                })  

            if user_data:
                return jsonify({
                    'success': True,
                    'user_data': user_data
                })
        else:
            return jsonify({
                'success': False,
                'error': 'No users found'
            })

    except Exception as e:
        print(f"An error occured while trying to search: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to search'})


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

        existing_repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

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
    repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

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

        repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

        if not repository:
            return jsonify({'success': False, 'error': 'Could not delete repository'})
        
        repository_db.remove((User.user == username) and (User.repository_name == repository_name))

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

        repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

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
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

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
                                 (User.user == username) and (User.repository_name == repository_name))
            
            return jsonify({'success': True})
        else:
            allowed_extensions_list = ', '.join(ALLOWED_EXTENSIONS)
            return jsonify({'success': False, 'error': f'File type not allowed. Allowed types: {allowed_extensions_list}'})
        
    except Exception as e:
        print(f"An error occured while trying to add text to the repository: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to add text to the repository'})
    

@app.route('/view_file/<repository_name>/<stored_filename>')
def view_file(repository_name, stored_filename):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

    if not repository:
        return redirect(url_for('view_repository'))
    
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


@app.route('/delete_file', methods=['POST'])
def delete_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try: 
        username = session['username']
        repository_name = request.form['repository_name']
        stored_filename = request.form['stored_filename']
        repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

        print(repository_name)

        if not repository:
            return jsonify({'sccuess': False, 'error': 'Repository not found'})
        
        files = repository.get('files', [])
        updated_files = []
        file_to_delete = None

        for file in files: 
            if file['stored_filename'] == stored_filename:
                file_to_delete = file
            else:
                updated_files.append(file)

        if not file_to_delete:
            return jsonify({'success': False, 'error': 'File not found'})
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        repository_db.update({'files': updated_files},
                             (User.user == username) and (User.repository_name == repository_name))
        
        return jsonify({'success': True})

    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occurred while trying to delete the file'})


@app.route('/download_file/<repository_name>/<stored_filename>', methods=['POST', 'GET'])
def download_file(repository_name, stored_filename):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        username = session['username']
        repository = repository_db.get((User.user == username) and (User.repository_name == repository_name))

        if not repository:
            return jsonify({'success': False, 'error': 'Could not find repository'})
        
        file_info = None
        for file in repository.get('files', []):
            if file['stored_filename'] == stored_filename:
                file_info = file
                break

        if not file_info:
            return jsonify({'success': False, 'error': 'File not found'})
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)

        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'The path to the file does not exist'})
        
        return send_file(
            file_path,
            mimetype=None,
            as_attachment=True,
            download_name=file_info['original_filename']
        )


    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occured while trying to download the file'})
    

@app.route('/add_friend', methods=['POST'])
def add_friend():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        current_username = session['username']
        add_friend_username = request.form['add_friend_username']
        added_friend_exist = user_table.get(User.username == add_friend_username)

        if not added_friend_exist:
            return jsonify({'success': False, 'error': f'Could not find user {add_friend_username} to add them as a friend'})
        
        if current_username == add_friend_username:
            return jsonify({'success': False, 'error': 'You cannot add yourself as a friend!'})
        
        current_user = user_table.get(User.username == current_username)
        if not current_user:
            return jsonify({'success': False, 'error': 'Current user not found'})

        friends = current_user.get('friends', [])

        if add_friend_username in friends:
            return jsonify({'success': False, 'error': f'{add_friend_username} is already your friend'})
        

        friends.append(add_friend_username)

        user_table.update({'friends': friends}, (User.username == current_username))
        
        return jsonify({'success': True})

    except Exception as e:
        print(f"Error adding {add_friend_username} as friend: {str(e)}")
        return jsonify({'success': False, 'error': f'An error occured while trying to add {add_friend_username} as friend'})


if __name__ == "__main__":
    # Ustvari direktorij za predloge, če ne obstaja
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app.run(debug=True)
    