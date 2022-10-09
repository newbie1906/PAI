# Dołączanie modułu flask 

from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3

# Tworzenie aplikacji
app = Flask("Flask - Lab")

# Ścieżka do pliku bazy danych w sqlite
DATABASE = 'database.db'



@app.route('/create_database', methods=['GET', 'POST'])
def create_db():
    # Połączenie sie z bazą danych
    conn = sqlite3.connect(DATABASE)
    # Stworzenie tabeli w bazie danych za pomocą sqlite3
    conn.execute('CREATE TABLE users (username TEXT, password TEXT)')
    # Zakończenie połączenia z bazą danych
    conn.close()
    
    return index()

@app.route('/', methods=['GET', 'POST'])
def index():
    con = sqlite3.connect(DATABASE)
    
    # Pobranie danych z tabeli
    cur = con.cursor()
    cur.execute("select * from users")
    users = cur.fetchall(); 

    return render_template('t4.html', users = users)


@app.route('/add', methods=['POST'])
def add():
        login = request.form['login']
        password = request.form['password']


        # Dodanie użytkownika do bazy danych
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)",(login,password) )
        con.commit()
        con.close()

        return "Dodano użytkownika do bazy danych <br>" + index()

# Uruchomienie applikacji w trybie debug
app.run(debug = True)