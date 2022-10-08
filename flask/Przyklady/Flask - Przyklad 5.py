# Dołączanie modułu flask 

from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask import Flask, session
from flask_session import Session

# Tworzenie aplikacji
app = Flask("Flask - Lab")

# Tworzenie obsługi sesji
sess = Session()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Sprawdzenie czy w sesji dla danego klienta zapisana jest nazwa użytkownika
    if 'user' in session:
        return render_template('t3.html', userdata=session['user'])
    else:
        return render_template('t1.html')


@app.route('/login', methods=['POST'])
def login():
    # Stworzenie sesji dla kilenta i dodanie pola user
    session['user']="username"
    return "Sesja została utworzona <br> <a href='/'> Dalej </a> "


@app.route('/logout', methods=['GET'])
def logout():
    # Jeżeli sesja klienta istnieje - usunięcie sesji 
    if 'user' in session:
        session.pop('user')
    else:
        # Przekierowanie klienta do strony początkowej
        redirect(url_for('index'))
    
    return "Wylogowano <br>  <a href='/'> Powrót </a>"

# Uruchomienie aplikacji w trybie debug
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.debug = True
app.run()