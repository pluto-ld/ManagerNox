from flask import Flask, render_template, url_for, request, flash, redirect
from markupsafe import escape  # Here just in case, for later use.
from werkzeug.utils import secure_filename
import flaskwebgui
import sqlite3
import os

# Add macros.
# TODO: Later on, need to add a gallery option to save additional images of characters.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Only images are allowed currently.
ICON_FOLDER = 'static/images/icons'
DEFAULT_ICON = '../static/images/icons/0.png'

app = Flask(__name__)  # Application name.
gui = flaskwebgui.FlaskUI(app=app, server="flask", width=800, height=600)  # GUI. Out of web browser display.
app.config['SECRET_KEY'] = '01ed46a4097a453509ab911c81a2c1d6745189fb1eb9921d'  # Necessary for flash messages
app.config['ICON_FOLDER'] = ICON_FOLDER
#app.config['MAX_UPLOAD'] = 16 * 1000 * 1000  # 16 MB TODO: make a maximum file size config

# UTILITY FUNCTIONS

# Get the database. This is used for display on the front page.
# TODO: When it comes to adding folders, likely add a 'folders' column and search via that?
def get_db():
    cn = sqlite3.connect('database/database.db')
    cn.row_factory = sqlite3.Row  # Get characters by row (makes them accessible via name or by index)
    return cn

# Get a character's information from the database.
# TODO: Change to getting character by ID. Character name is changeable and can be injected, this theoretically
# would prevent losing them.
def get_info_by_name(chara_name):
    cn = get_db()
    info = cn.execute("SELECT * FROM character WHERE cname = ?", (chara_name,)).fetchone()  # Get info based on name.
    cn.close()

    if info is None:
        return redirect('home')  # If page doesn't exist, just go home. TODO: Proper error handling.

    return info

# Check if filetype is allowed.
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ROUTES

# Homepage.
@app.route("/")  # Go to localhost. This binds the below function when you go to this URL, and so it runs this function when it starts up.
def home():
    cn = get_db()
    characters = cn.execute("SELECT * FROM character").fetchall()  # Fetch characters from database.
    cn.close()
    return render_template('index.html', characters=characters)  # Get render template, display database of characters on it.

# Character profile loader. Loads the character you select!
@app.route("/character/<chara_name>")
def show_character_profile(chara_name):
    return render_template('profile.html', info=get_info_by_name(chara_name))  # Create the create page; get information by character name to display.

# Create page. Needs to get all of the information you want it to, then adds the character to your database!
# TODO: image upload, add text to database, default icon.
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == 'POST':
        # Adding icon:
        iconpath = DEFAULT_ICON # Start with the default icon.
        
        # Check if post request has the file part.
        if 'icon' not in request.files:
            pass # Pass if it's not in the request files.
        elif 'icon' in request.files:
            icon = request.files['icon']
            if icon.filename == '':
                pass  # Pass if the filename is empty. This is to keep the default icon path intact.
            elif icon and allowed_file(icon.filename):
                iconname = secure_filename(icon.filename)
                icon.save(os.path.join(app.config['ICON_FOLDER'], iconname))
                iconpath = "../" + ICON_FOLDER+"/"+iconname  # Create the path to the icon so it can be stored.

        # Get rest of information (all text) from form.
        cname = request.form['name']
        gender = request.form['gender']
        race = request.form['race']
        personality = request.form['personality']
        backstory = request.form['backstory']
        
        # Check to see if there is a name. This is the only required field.
        if not cname:
            flash('Name is required.')
        else:
            cn = get_db()
            cn.execute('INSERT INTO character (icon, cname, gender, race, personality, backstory) VALUES (?, ?, ?, ?, ?, ?)',  # The table is set up so that defaults will be NULL.
                    (iconpath, cname, gender, race, personality, backstory))  # You should be able to just add characters w/o filling every field.
            # TODO: When adding new or custom fields, use if statements instead to build the character row?
            cn.commit()
            cn.close()
            return redirect(url_for('home'))  # Return home
    
    return render_template('create.html')  # Create the create page.

# Edit page. Ideally, final version of this will look almost exactly like the character profile pages!
@app.route('/character/<chara_name>/edit', methods=('GET', 'POST'))
def edit(chara_name):
    info = get_info_by_name(chara_name)
    # TODO: This and create's form are the same now. Ideally this should be changed so that the code isn't duplicated.
    if request.method == 'POST':
        # Default icon should stay as this.
        iconpath = info['icon']  # Get original icon's filepath.

        # Check if post request has the file part.
        if 'icon' not in request.files:
            pass # Pass if it's not in the request files.
        elif 'icon' in request.files:
            icon = request.files['icon']
            if icon.filename == '':
                pass  # Pass if the filename is empty. TODO: change to throw an error, update other when it happens.
            elif icon and allowed_file(icon.filename):
                iconname = secure_filename(icon.filename)
                icon.save(os.path.join(app.config['ICON_FOLDER'], iconname))
                # TODO: Delete old profile picture to save space.
                iconpath = "../" + ICON_FOLDER+"/"+iconname  # Create the path to the icon so it can be stored.

        cname = request.form['name']  # Fill out text areas.
        gender = request.form['gender']
        race = request.form['race']
        personality = request.form['personality']
        backstory = request.form['backstory']
        
        # Check to see if there is a name. This is the only required field.
        if not cname:
            flash('Name is required.')  # TODO: Get flash messages working.
        else:
            cn = get_db()
            cn.execute('UPDATE character SET icon = ?, cname = ?, gender = ?, race = ?, personality = ?, backstory = ? WHERE id = ?',  # The table is set up so that defaults will be NULL.
                    (iconpath, cname, gender, race, personality, backstory, info['id']))  # Uses ID instead of character name; ID can't be changed so it's more reliable to fetch information if name is changed.
            cn.commit()
            cn.close()
            return redirect(url_for('show_character_profile', chara_name=cname))  # Return to the character's profile.
    
    return render_template('edit.html', info=get_info_by_name(chara_name))

if __name__ == '__main__':  # Run main and launch the app.
    #app.run(debug=True)  # Browser version; use for debugging!
    gui.run()