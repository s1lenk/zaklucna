# GitHub but Worse - A Simple Git Repository Manager

A lightweight Flask-based web application that mimics basic GitHub functionality, allowing users to create repositories, upload files, and manage their code projects locally.

## Features

- **User Authentication**: Simple login/registration system
- **Repository Management**: Create, view, and delete repositories
- **File Operations**: Upload, view, download, and delete files
- **File Type Support**: Support for various file types (Python, HTML, CSS, JavaScript, JSON, etc.)
- **Syntax Highlighting**: Code syntax highlighting for better readability
- **Community Features**: Search for other users
- **Responsive Design**: Clean and intuitive web interface

## Prerequisites

Before running this application, make sure you have the following installed on your system:

- **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)

## Installation & Setup

### 1. Clone or Download the Project

If you have the project files, place them in a directory of your choice.

### 2. Navigate to Project Directory

```bash
cd path/to/your/project/directory
```

### 3. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If the above command doesn't work, install the dependencies manually:

```bash
pip install Flask tinydb
```

### 5. Run the Application

```bash
python main.py
```

The application will start and you should see output similar to:

```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 6. Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

or

```
http://localhost:5000
```

## Usage

### Getting Started

1. **Login/Register**: When you first visit the application, you'll be redirected to the login page. Enter a username and password - if the account doesn't exist, it will be created automatically.

2. **Create Repository**: From the main page, enter a repository name and click "Create repository".

3. **Upload Files**: Navigate to your repository and use the file upload feature to add files.

4. **Manage Files**: View, download, or delete files as needed.

### Supported File Types

The application supports the following file extensions:
- `.py` (Python)
- `.html` (HTML)
- `.css` (CSS)
- `.js` (JavaScript)
- `.txt` (Text)
- `.md` (Markdown)
- `.json` (JSON)
- `.xml` (XML)
- `.csv` (CSV)

## Project Structure

```
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
```

## Configuration

### File Upload Limits
- Maximum file size: 16MB
- Files are stored in the `uploads/` directory

### Database
The application uses TinyDB (JSON-based database) for data storage:
- User data: `static/json/user.json`
- Repository data: `static/json/repositories.json`

### Security Note
This application is designed for local development and educational purposes. The authentication system is basic and should not be used in production environments.

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port by modifying the last line in `main.py`:
   ```python
   app.run(debug=True, port=5001)  # Use a different port
   ```

2. **Permission errors with file uploads**:
   - Ensure the application has write permissions in the project directory

3. **Missing dependencies**:
   - Make sure all packages from `requirements.txt` are installed
   - Try upgrading pip: `pip install --upgrade pip`

4. **JSON database corruption**:
   - Delete the JSON files in `static/json/` to reset the database
   - The files will be recreated automatically

### Development Mode

The application runs in debug mode by default, which means:
- Automatic reloading when code changes
- Detailed error messages
- Debug information in the console

To disable debug mode, change the last line in `main.py`:
```python
app.run(debug=False)
```

## Features Overview

### User Management
- Simple registration (automatic account creation)
- Session-based authentication
- User search functionality

### Repository Features
- Create repositories with custom names
- View repository contents
- Delete repositories
- Date tracking for creation

### File Management
- Upload multiple file types
- Syntax highlighting for code files
- File download functionality
- File deletion with confirmation
- File size and upload date tracking

## Contributing

This is a student project (3rd year final project - "zaklucna za 3. letnik"). Feel free to fork and modify according to your needs.

## License

This project is created for educational purposes. Use and modify as needed for learning and development.

## Future Improvements

Potential enhancements that could be added:
- User profiles and avatars
- Repository collaboration features
- Version control functionality
- File editing capabilities
- Advanced search features
- Email notifications
- API endpoints
- Docker containerization

---

**Note**: This application is a simplified version of GitHub functionality and is intended for educational purposes and local development use.