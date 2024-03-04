import os
from Model.PySQLite import PySQLiteConnection
from flask import Flask, render_template, request, session

template_dir = database_dir = static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
for p in ['Web_App_Flask_Apache', 'View', 'Templates']:
    template_dir = os.path.join(template_dir, p)
for d in ['Web_App_Flask_Apache', 'Model', 'Database', 'database.sqlite']:
    database_dir = os.path.join(database_dir, d)
for s in ['Web_App_Flask_Apache', 'View', 'Static']:
    static_dir = os.path.join(static_dir, s)

db = PySQLiteConnection.PySQLiteConnection(database_dir)

app = Flask(__name__, static_url_path='', static_folder=static_dir, template_folder=template_dir)
app.secret_key = '1986420918283627'
print(static_dir)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('index.html') 

@app.route('/create')
def create():
    return "TODO"

@app.route('/main', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        # Check the login credentials
        if db.checkPasswort((login, password)):
            # Save the login status in the session
            session['logged_in'] = True
            return render_template('main.html')
        else:
            session['logged_in'] = False
            return render_template('login.html')
    else:
        if session['logged_in']:
            return render_template('main.html')
        else:
            return render_template('login.html')
    return "TODO page visible for logged user"

if __name__ == '__main__':
    app.run()
