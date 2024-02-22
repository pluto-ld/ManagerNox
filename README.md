# ManagerNox
Manager Nox is an offline-first desktop application for storing your original characters.

Made as an offline alternative to character databases such as toyhou.se, Campfire, and CharacterHub.

# Technical
This application uses Flask and SQLite, as well as PSutil, FlaskWebGUI. The frontend is HTML, CSS, and Jinja. Packaged with PyInstaller.

## Requirements:
- Python >= 3.11
- Flask = 3.0.2
- flaskwebgui = 1.0.9
- and more; all are listed in the requirements.txt file.

## Setup
- Run pip install -r requirements.txt to install dependencies.
- Run init_db.py to start the database. Any images and the previous database (database.db) should be removed manually first! (Will add an easier reset later.)

## Running it
- Run python3 app.py or py app.py.

# Features
## Current
- Create, edit, and view characters.

## Planned features
This list is in order of priority, and primarily used for tracking development.
- Remove characters
- Reset database
- Backup creation
- Search
- Folders
- Character image galleries
- Custom fields
- Character tags