from http.client import REQUEST_ENTITY_TOO_LARGE
import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask_session import Session


DATABASE = "ksiazki.sqlite"

app = Flask("spis ksiazek")
app.secret_key = 'Is this the real life? Is this just fantasy? No escape from reality'
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)
app.config.from_object(__name__)



# conn = sqlite3.connect(DATABASE)
# conn.execute("create table if not exists users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT, isAdmin INTEGER)")
# conn.execute("create table if not exists item (name TEXT)")
# conn.execute("insert into users (username, password, isAdmin) values ('soviet', 'password', 1)")
# conn.commit()
# conn.close()

@app.route('/', methods=["GET", "POST"])
def index():
    if 'user' in session:
        con=sqlite3.connect(DATABASE)
        cur = con.cursor()
        if request.method == 'GET':
            isAdmin= False
            if session['role'] == 'admin':
                isAdmin = True
            cur.execute('Select * from item')
            ksiazki = cur.fetchall()
            con.close()
            if 'message' in session:
                message = session['message']
                session.pop('message')
                return render_template('book_list.html', ksiazki=ksiazki, isAdmin=isAdmin, message=message)
            else:
                return render_template('book_list.html', ksiazki=ksiazki, isAdmin=isAdmin)
        if request.method == 'POST':
            cur.execute("insert into item(name) values (?)", (request.form['title'],))
            con.commit()
            con.close()
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            return render_template('register.html', data='Login i hasło są wymagane')
        else: 
            username = request.form['username']
            password = request.form['password']
            if session['role'] == 'admin':
                isAdmin = 'isAdmin' in request.form
            else:
                isAdmin = 0
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('select username from users where username=?', (username,))
            if cur.fetchone() is not None:
                if session['role'] == 'admin':
                    session['message'] = 'Użytkownik już istnieje'
                    return redirect(url_for('admin_panel'))
                return render_template('register.html', data='Użytkownik już istnieje')
            cur.execute('insert into users (username, password, isAdmin) values (?, ?, ?)', (username, password, isAdmin))
            conn.commit()
            conn.close()
            if session['role'] == 'admin':
                return redirect(url_for('admin_panel'))
            return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            return render_template('login.html', data='Login i hasło są wymagane')
        else:    
            username = request.form['username']
            password = request.form['password']
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            try:
                cur.execute("select password, isAdmin from users where username = ?", (username,))
            except sqlite3.Error as err:
                return render_template('login.html', data='Cos nie pyklo w bazie' )
            user = cur.fetchone()
            if password == user[0]:
                session['user'] = username
                if user[1] == 1:
                    session['role'] = 'admin'
                else:
                    session['role'] = 'user'
                return redirect(url_for('index'))
            else: 
                return render_template('login.html', data='Błędny login lub hasło')

@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        session.pop('role')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/super_secret_url_unavailable_for_mere_mortals', methods=['GET'])
def admin_panel():
    if session['role'] == 'admin':
        if request.method == 'GET':
            con=sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("select * from users")
            users = cur.fetchall()
            con.close()
            if 'message' in session:
                message = session['message']
                session.pop('message')
                return render_template('admin_panel.html', users=users, message=message)
            return render_template('admin_panel.html', users=users)

    else:
        session['message'] = 'U mere mortal do not deserve to see my precious admin panel'
        return redirect(url_for('index'))

@app.route('/users/<username>')
def user_name(username):
    con=sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("select * from users where username = ?", (username,))
    user = cur.fetchone()
    return render_template('user_details.html', user=user)

@app.route('/users/<int:id>')
def user_id(id):
    con=sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("select * from users where user_id = ?", (id,))
    user = cur.fetchone()
    return render_template('user_details.html', user=user)



app.run(debug=True)