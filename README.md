GitHub but Worse - A Simple Git Repository Manager
A lightweight Flask-based web application that mimics basic GitHub functionality, allowing users to create repositories, upload files, and manage their code projects locally.
Features

User Authentication: Simple login/registration system
Repository Management: Create, view, and delete repositories
File Operations: Upload, view, download, and delete files
File Type Support: Support for various file types (Python, HTML, CSS, JavaScript, JSON, etc.)
Syntax Highlighting: Code syntax highlighting for better readability
Community Features: Search for other users
Responsive Design: Clean and intuitive web interface

Prerequisites
Before running this application, make sure you have the following installed on your system:

Python 3.7+ - Download Python
pip - Python package installer (usually comes with Python)

Installation & Setup
1. Clone or Download the Project
If you have the project files, place them in a directory of your choice.
2. Navigate to Project Directory
bashcd path/to/your/project/directory
3. Create a Virtual Environment (Recommended)
bash# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
4. Install Dependencies
bashpip install -r requirements.txt
If the above command doesn't work, install the dependencies manually:
bashpip install Flask tinydb
5. Run the Application
bashpython main.py
The application will start and you should see output similar to:
* Running on http://127.0.0.1:5000
* Debug mode: on
6. Access the Application
Open your web browser and navigate to:
http://127.0.0.1:5000
or
http://localhost:5000
Usage
Getting Started

Login/Register: When you first visit the application, you'll be redirected to the login page. Enter a username and password - if the account doesn't exist, it will be created automatically.
Create Repository: From the main page, enter a repository name and click "Create repository".
Upload Files: Navigate to your repository and use the file upload feature to add files.
Manage Files: View, download, or delete files as needed.

Supported File Types
The application supports the following file extensions:

.py (Python)
.html (HTML)
.css (CSS)
.js (JavaScript)
.txt (Text)
.md (Markdown)
.json (JSON)
.xml (XML)
.csv (CSV)

Project Structure
zaklucna/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/
│   ├── css/
│   │   └── style.css      # Application styles
│   └── json/
│       ├── user.json      # User data storage
│       └── repositories.json # Repository data storage
├── templates/             # HTML templates
│   ├── login.html
│   ├── mainPage.html
│   ├── repository.html
│   ├── view_file.html
│   ├── account_settings.html
│   └── community_page.html
└── uploads/               # Uploaded files storage (created automatically)
Configuration
File Upload Limits

Maximum file size: 16MB
Files are stored in the uploads/ directory

Database
The application uses TinyDB (JSON-based database) for data storage:

User data: static/json/user.json
Repository data: static/json/repositories.json

Security Note
This application is designed for local development and educational purposes. The authentication system is basic and should not be used in production environments.
Troubleshooting
Common Issues

Port already in use:

Change the port by modifying the last line in main.py:

pythonapp.run(debug=True, port=5001)  # Use a different port

Permission errors with file uploads:

Ensure the application has write permissions in the project directory


Missing dependencies:

Make sure all packages from requirements.txt are installed
Try upgrading pip: pip install --upgrade pip


JSON database corruption:

Delete the JSON files in static/json/ to reset the database
The files will be recreated automatically



Development Mode
The application runs in debug mode by default, which means:

Automatic reloading when code changes
Detailed error messages
Debug information in the console

To disable debug mode, change the last line in main.py:
pythonapp.run(debug=False)